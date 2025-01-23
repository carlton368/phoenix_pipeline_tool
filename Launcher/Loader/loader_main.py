import sys
import os
import math
import shutil
import subprocess
import platform
import shlex
import shutil
import logging
import traceback
from pprint import pprint
from typing import Optional, List, Dict, Any, Tuple
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit,
    QTableWidget, QTreeWidget, QStackedWidget, QTreeWidgetItem, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QFrame, QHeaderView, QTabWidget
)
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QGuiApplication
from Launcher.Loader.ui_loader_mockup_v5 import Ui_Form
from Launcher.Loader.loader_dataexplorer import DataExplorer, ThumbnailManager, DataManagerForSaver
from Launcher.Loader.loader_entity_handlers import AssetHandler, ShotHandler
from Launcher.Loader.loader_config_manager import ConfigManager
from core.shotgun_api_client import ShotGunAPIclient
import shotgun_api3
from PySide6.QtWidgets import QMessageBox
import datetime



#Shotgun Methods of Entity Operations(엔티티 작업 관련 Shotgun 메서드)
class SGEntityoperator():
    """ ShotGun Entity Operator 클래스 """
    _instance = None
    def __new__(cls):   # init 전에 호출되는 클래스 메소드! self가 아니라 cls를 인자로 받는다.
        if not cls._instance:   # 인스턴스가 없으면
            cls._instance = super().__new__(cls)    # 부모 클래스(object)의 __new__ 메소드 호출
            cls._instance.initialize_shotgun_api()
        return cls._instance

    def initialize_shotgun_api(self):   # Shotgun API 초기화 메서드
        print("<SGEntityoperator>  Shotgun API 초기화 중...")
        self.shotgunAPIclient = ShotGunAPIclient()   # ShotGunAPIclient 인스턴스 생성
        self.sg = self.shotgunAPIclient.shotgun_api_object()   # Shotgun API 객체 가져오기

    def read_shotgun_entity(self, entity_type: str, entity_id: int) -> Dict[str, Any]:
        """
        Read an entity from Shotgun.
        :param entity_type: The type of entity to read.
        :param entity_id: The id of the entity to read.
        :return: The entity data.
        """
        try:
            result = self.sg.find_one(entity_type, [["id", "is", entity_id]])
            if result:
                print(f"<SGEntityoperator> Read {entity_type} entity with id {entity_id}")
            else:
                print(f"<SGEntityoperator> {entity_type} entity with id {entity_id} not found")
            return result
        except Exception as e:
            print(f"<SGEntityoperator> Failed to read {entity_type} entity with id {entity_id}: {e}")
            return {}

    def update_shotgun_entity(self, entity_type: str, entity_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an entity in Shotgun.
        :param entity_type: The type of entity to update.
        :param entity_id: The id of the entity to update.
        :param data: The updated data for the entity.
        :return: The updated entity data.
        """
        try:
            result = self.sg.update(entity_type, entity_id, data)
            print(f"<SGEntityoperator> Updated {entity_type} entity with id {entity_id}")
            return result
        except Exception as e:
            print(f"<SGEntityoperator> Failed to update {entity_type} entity with id {entity_id}: {e}")
            return {}

    def delete_shotgun_entity(self, entity_type: str, entity_id: int) -> bool:
        """
        Delete an entity from Shotgun.
        :param entity_type: The type of entity to delete.
        :param entity_id: The id of the entity to delete.
        :return: True if the entity was deleted successfully, False otherwise.
        """
        try:
            self.sg.delete(entity_type, entity_id)
            print(f"<SGEntityoperator> Deleted {entity_type} entity with id {entity_id}")
            return True
        except Exception as e:
            print(f"<SGEntityoperator> Failed to delete {entity_type} entity with id {entity_id}: {e}")
            return False

########################################################################################################################

class VersionItemWidget(QWidget):
    """버전 아이템 위젯 클래스"""
    def __init__(self, thumbnail_path: str, version_code: str, is_grid_view: bool = False, parent=None):    # 썸네일 경로, 버전 코드, 그리드 뷰 여부, 부모 위젯
        super().__init__(parent)    # 부모 클래스 생성자 호출
        self.thumbnail_path = thumbnail_path    # 썸네일 경로
        if is_grid_view:    # 그리드 뷰인 경우
            layout = QVBoxLayout(self)  # 수직 박스 레이아웃
            layout.setAlignment(Qt.AlignCenter)
            thumbnail_size = 100    # 썸네일 크기
            # self.setFixedSize(120, 150)   # 위젯 크기 설정
        else:
            layout = QHBoxLayout(self)  # 수평 박스 레이아웃
            layout.setAlignment(Qt.AlignCenter)
            thumbnail_size = 50   # 썸네일 크기
            self.setFixedHeight(60) # 위젯 높이 설정
        
        self.thumbnail_label = QLabel() # 썸네일 레이블
        # self.thumbnail_label.setFixedSize(thumbnail_size, thumbnail_size)   # 썸네일 크기 설정
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)  # 중앙 정렬 추가
        
        if thumbnail_path:  # 썸네일 경로가 있을 때
            pixmap = QPixmap(thumbnail_path)    # 썸네일 이미지 로드
            if not pixmap.isNull(): # 이미지가 유효할 때
                scaled_pixmap = pixmap.scaledToWidth(200)
                self.thumbnail_label.setPixmap(scaled_pixmap)
                self.thumbnail_label.setScaledContents(True)
                # self.thumbnail_label.setPixmap(pixmap.scaled(thumbnail_size, thumbnail_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # 썸네일 이미지 설정
            else:
                self.thumbnail_label.setText("Invalid Image")   # 이미지가 유효하지 않을 때 "Invalid Image" 텍스트 표시
                print("Error: Invalid Image")   
        else:
            # 이미지가 없을 때 "No Image" 텍스트 표시
            self.thumbnail_label.setText("No Image")
            self.thumbnail_label.setFixedSize(160, 110)
            self.thumbnail_label.setStyleSheet("background-color: #f0f0f0; color: #888888;")  # 배경색과 텍스트 색상 설정
        
        self.version_label = QLabel(version_code)   # 버전 코드(이름) 레이블
        self.version_label.setWordWrap(True)
        # self.version_label.setAlignment(Qt.AlignCenter if is_grid_view else Qt.AlignVCenter | Qt.AlignLeft) # 중앙 또는 왼쪽 정렬 설정
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        
        layout.addWidget(self.thumbnail_label)  # 썸네일 레이블 추가
        layout.addWidget(self.version_label)    # 버전 코드(이름) 레이블 추가
        layout.setContentsMargins(5, 5, 5, 5)   # 레이아웃 여백 설정
        self.setLayout(layout)  # 위젯 레이아웃 설정

class MainWindow(QWidget):

    current_project_id: Optional[int] = None           # 현재 선택된 프로젝트 ID
    current_project_info: Dict[str, Any] = {}          # 현재 선택된 프로젝트 정보
    current_entity_type: Optional[str] = None          # 현재 선택된 엔티티 타입 (Asset 또는 Shot)
    current_view_mode: str = 'initial_grid_view'       # 현재 뷰 모드 (initial_grid_view, advanced_grid_view, list_view)
    current_task_id: Optional[int] = None              # 현재 선택된 태스크 ID
    current_version_data: Optional[Dict[str, Any]] = None   # 현재 선택된 버전 데이터
    current_thumbnail_path: Optional[str] = None       # 현재 선택된 썸네일 경로
    current_path_info: Dict[str, Any] = {}             # 현재 선택된 경로 정보
    current_version_info: Dict[str, Any] = {}          # 현재 선택된 버전 정보
    current_publish_info: Dict[str, Any] = {}          # 현재 선택된 Publish 정보
    current_viewer_tab_index: int = 0                         # 현재 선택된 탭 인덱스
    # current_entity_id: Optional[int] = None            # 현재 선택된 엔티티 ID
    nuke_validator_instance = None                      # NukeValidator 인스턴스

    

    def __init__(self, email: Optional[str] = None, shotgun_client: Optional[ShotGunAPIclient] = None): # 이메일, Shotgun 객체 인자로 받음 
        """
        메인 윈도우 초기화 메서드
        :param email: 사용자 이메일
        :param sg: Shotgun 객체
        """
        super().__init__()
        print("메인 윈도우 초기화 중...")
        self.setup_search_mode()                        # 검색 기능 세팅!!!!!!!!!!!!!!!!!!!!!!!!!!
        if shotgun_client:  # Shotgun API 객체가 있을 때
            self.shotgun_api_client = shotgun_client    # ShotGunAPIclient 전달 받기
        else:
            self.shotgun_api_client = ShotGunAPIclient()    # ShotGunAPIclient 인스턴스 생성
        self.sg = self.shotgun_api_client.shotgun_api_object()  # Shotgun API 객체 가져오기
        self.ensure_shotgun_api_object_exit()  # Shotgun API 객체 생성 확인
        self.data_explorer = DataExplorer(sg=self.sg, email=email)  # DataExplorer 인스턴스 생성
        self.instanceing_modules_classes()   # 모듈 클래스 인스턴스
        self.base_path = self.config.get_base_path() 
        self.ui.setupUi(self)                          # UI 설정
        self.setup_ui()                                # UI 설정
        self.setup_home_page()                         # 홈 페이지 설정
        self.setup_connections()                       # 이벤트 연결 설정
        self.update_user_name()                        # 사용자 이름 업데이트
        self.set_window_to_center()
        self.go_home()                                 # 홈 페이지로 이동
        print("메인 윈도우 초기화 완료.")

    def set_window_to_center(self):  # 창 가운데 띄우기
        window_frame = self.frameGeometry()
        screen_center = QGuiApplication.primaryScreen().availableGeometry().center()
        window_frame.moveCenter(screen_center)
        self.move(window_frame.topLeft())
    def ensure_shotgun_api_object_exit(self):    # Shotgun API 객체 생성 확인 메서드
        """ Shotgun API 객체 생성 확인 및 생성될 때까지 재시도 """
        check = self.sg == None    # Shotgun API 객체 생성 여부 확인
        print("<MainWindow> Shotgun API is exist: ", check)
        
        if not check:   # Shotgun API 객체가 생성되지 않았을 때
            try:
                check = self.shotgun_api_client.is_shotgun_api_object_created(self.sg)    # Shotgun API 객체 생성 여부 확인
                print("<MainWindow> Shotgun API is created: ", check)   # Shotgun API 객체 생성 여부 출력
            except Exception as e:
                print(f"<MainWindow> Shotgun API 객체 생성 실패: {e}")
        if not check:   # Shotgun API 객체가 생성되지 않았을 때
            print("<MainWindow> Shotgun API 객체 없음. 다시 생성 중...")
            try:
                self.shotgun_api_client.initialize_shotgun_api_client()   # Shotgun API 객체 생성
                self.sg = self.shotgun_api_client.shotgun_api_object()   # Shotgun API 객체 가져오기
                check = self.shotgun_api_client.is_shotgun_api_object_created(self.sg)    # Shotgun API 객체 생성 여부 확인
                print("<MainWindow> Shotgun API is created: ", check)   # Shotgun API 객체 생성 여부 출력
            except Exception as e:
                print(f"<MainWindow> Shotgun API 객체 생성 실패: {e}")
        else:
            print("<MainWindow> Shotgun API 객체 있음.") # Shotgun API 객체가 생성되어 있을 때
        if not check:   # Shotgun API 객체가 생성되지 않았을 때
            try:
                self.config = ConfigManager()                  # ConfigManager 인스턴스 생성
                self.sg = shotgun_api3.Shotgun(
                self.config.get_value_as_str('Shotgun', 'shotgun_url'),
                self.config.get_value_as_str('Shotgun', 'admin_script_name'),
                self.config.get_value_as_str('Shotgun', 'admin_api_key'))
                check = self.sg is not None
            except Exception as e:
                print(f"<MainWindow> Shotgun API 객체 생성 실패: {e}")
        if not check:   # Shotgun API 객체가 생성되지 않았을 때
            self.sg = self.shotgun_api_client.emergency_shotgun_api_object_creation()   # 비상용 Shotgun API 객체 생성
            print("<MainWindow> 비상용 Shotgun API 객체 생성 완료")
        print("<MainWindow> Shotgun API 객체 생성 확인 완료.")
            
    def setup_search_mode(self):
        print("검색 모드 설정 중...")
        self.search_timer = QTimer(self)    # 검색 타이머 생성
        self.search_timer.setSingleShot(True)   # 한 번만 실행되도록 설정
        self.search_timer.timeout.connect(self.perform_search)  # 타임아웃 시 perform_search 메서드 호출
        self.current_search_widget = None  # 현재 검색 중인 위젯을 추적하는 변수 추가
        print("검색 타이머 설정 완료")

    def instanceing_modules_classes(self):
        print("모듈 클래스 인스턴스화 중...")
        self.config = ConfigManager()
        self.shotgun_api_client = ShotGunAPIclient()   # ShotGunAPIclient 인스턴스 생성(싱글톤)
        self.sg_entity_operator = SGEntityoperator()    # SGEntityoperator 인스턴스 생성(싱글톤)
        self.thumbnail_manager = ThumbnailManager(sg=self.sg)  # ThumbnailManager 인스턴스 생성
        self.ui = Ui_Form()                            # UI 로더 인스턴스 생성
        self.asset_handler = AssetHandler(self)        # AssetHandler 인스턴스 생성
        self.shot_handler = ShotHandler(self)          # ShotHandler 인스턴스 생성
        self.data_manager_for_saver = DataManagerForSaver()        

    def setup_ui(self):
        print("UI 설정 중...")
        
        self.main_stacked_widget = self.ui.stackedWidget_main   # 메인 스택 위젯 (인덱스 0는 홈 페이지, 인덱스 1은 프로젝트 페이지)
        self.stackedWidget_sub = self.ui.stackedWidget_sub # 서브 스택 위젯 (인덱스 0은 이니셜 그리드 페이지, 인덱스 1은 어드밴스드 그리드 페이지, 인덱스 2는 리스트 페이지)
        self.tab_widget = self.ui.tabWidget     # 탭 위젯 (인덱스 0은 Tasks, 인덱스 1은 Assets, 인덱스 2은 Shots)
        self.second_tab_widget = self.ui.tabWidget_2   # 이니셜 그리드 뷰 탭 위젯 (인덱스 0은 Working, 인덱스 1은 Publishes)
        self.user_name_label = self.ui.label_username   # 로그인 유저 이름 레이블
        self.home_button = self.ui.pushButton_home      # 홈 버튼
        self.tabWidget_grid_full = self.ui.tabWidget_grid_full_wip  # 이니셜 그리드 뷰 탭 위젯 (인덱스 0은 Working, 인덱스 1은 Publishes)
        self.tableWidget_grid_advanced = self.ui.tabWidget_2    # 어드밴스드 그리드 뷰 탭 위젯 (인덱스 0은 Working, 인덱스 1은 Publishes)
        self.tableWidget_list = self.ui.tabWidget_3    # 리스트 뷰 탭 위젯 (인덱스 0은 Working, 인덱스 1은 Publishes)

        # 모든 뷰어 탭 위젯을 리스트로 저장
        self.all_viewer_tab_widgets = [
        self.tabWidget_grid_full,  # 초기 그리드 뷰의 탭 위젯
        self.tableWidget_grid_advanced,              # 어드밴스드 그리드 뷰의 탭 위젯
        self.tableWidget_list               # 리스트 뷰의 탭 위젯
        ]


        self.tableWidget_grid_full = self.ui.tableWidget_grid_full  # 이니셜 그리드 뷰 테이블 위젯 (Working)
        self.tableWidget_grid_full_pub = self.ui.tableWidget_grid_full_pub  # 이니셜 그리드 뷰 테이블 위젯 (Publishes)
        self.wip_table = self.ui.tableWidget_grid_wip   # 어드벤스드 그리드 뷰 테이블 위젯 (Working)
        self.pub_table = self.ui.tableWidget_grid_pub   # 어드벤스드 그리드 뷰 테이블 위젯 (Publishes)
        self.wip_list_table = self.ui.tableWidget_list_wip  # 리스트 뷰 테이블 위젯 (Working)
        self.pub_list_table = self.ui.tableWidget_list_pub  # 리스트 뷰 테이블 위젯 (Publishes)
        
        for table in [self.wip_table, self.pub_table, self.wip_list_table, self.pub_list_table, 
                      self.tableWidget_grid_full, self.tableWidget_grid_full_pub]:  # 모든 테이블 위젯에 대해
            table.setSelectionMode(QTableWidget.SingleSelection)    # 단일 선택 모드 설정 (한 번에 하나의 셀만 선택 가능)
            table.setEditTriggers(QTableWidget.NoEditTriggers)    # 편집 불가능 설정 (유저가 셀 내용 편집 불가)
            table.verticalHeader().setVisible(False)    # 수직 헤더 숨김
            table.horizontalHeader().setVisible(False)  # 수평 헤더 숨김
        
        self.project_name_label = self.ui.label_project_name    # 프로젝트 이름 레이블
        
        self.task_tree = self.ui.treeWidget_pathtree    # 마이 태스크 트리 위젯
        self.asset_tree = self.ui.treeWidget_Assets  # 에셋 트리 위젯
        self.shot_tree = self.ui.treeWidget_3    # 샷 트리 위젯
        
        self.tasks_search = self.ui.lineEdit_tasks_search
        self.assets_search = self.ui.lineEdit_assets_search
        self.shots_search = self.ui.lineEdit_shots_search
        self.version_search = self.ui.lineEdit_ver_search
        
        self.detail_page = QWidget()    # 상세 정보 페이지
        self.detail_layout = QVBoxLayout(self.detail_page)  # 상세 정보 페이지 레이아웃
        self.detail_frame = QFrame(self.detail_page)    # 상세 정보 프레임
        self.detail_layout.addWidget(self.detail_frame) # 상세 정보 페이지 레이아웃에 프레임 추가
        self.stackedWidget_sub.addWidget(self.detail_page)  # 서브 스택 위젯에 상세 정보 페이지 추가
        
        self.label_grid_asset_name = self.ui.label_grid_asset_name  # 어드밴스드 그리드 뷰 에셋 이름 레이블
        self.label_grid_asset_type = self.ui.label_grid_asset_type  # 어드밴스드 그리드 뷰 에셋 타입 레이블
        self.label_grid_asset_ver = self.ui.label_grid_asset_ver    # 어드밴스드 그리드 뷰 에셋 버전 레이블
        self.label_grid_asset_link = self.ui.label_grid_asset_link  # 어드밴스드 그리드 뷰 에셋 링크 레이블
        self.label_grid_asset_date = self.ui.label_grid_asset_date  # 어드밴스드 그리드 뷰 에셋 날짜 레이블
        self.label_grid_asset_artist = self.ui.label_grid_asset_artist  # 어드밴스드 그리드 뷰 에셋 아티스트 레이블
        self.label_grid_asset_des = self.ui.label_grid_asset_des    # 어드밴스드 그리드 뷰 에셋 설명 레이블
        
        self.label_list_asset_thumbnail = self.ui.label_list_asset_thumbnail    # 리스트 뷰 에셋 썸네일 레이블
        self.label_list_asset_name = self.ui.label_list_asset_name  # 리스트 뷰 에셋 이름 레이블
        self.label_list_asset_type = self.ui.label_list_asset_type  # 리스트 뷰 에셋 타입 레이블
        self.label_list_asset_ver = self.ui.label_list_asset_ver    # 리스트 뷰 에셋 버전 레이블
        self.label_list_asset_link = self.ui.label_list_asset_link  # 리스트 뷰 에셋 링크 레이블
        self.label_list_asset_date = self.ui.label_list_asset_date  # 리스트 뷰 에셋 날짜 레이블
        self.label_list_asset_artist = self.ui.label_list_asset_artist  # 리스트 뷰 에셋 아티스트 레이블
        self.label_list_asset_des = self.ui.label_list_asset_des    # 리스트 뷰 에셋 설명 레이블
        
        self.grid_button = self.ui.pushButton_grid  # 이니셜 그리드 뷰로 전환하는 버튼
        self.list_button = self.ui.pushButton_list  # 리스트 뷰로 전환하는 버튼
        
        self.stackedWidget_sub_grid = self.ui.stackedWidget_sub_grid    # 어드벤스 그리드 뷰용 메타데이터 서브 스택 위젯 (인덱스 0은 샷, 인덱스 1은 에셋)
        self.stackedWidget_sub_list = self.ui.stackedWidget_sub_list    # 리스트 뷰용 메타데이터 서브 스택 위젯 (인덱스 0은 샷, 인덱스 1은 에셋)
        
        self.label_list_shot_thumbnail = self.ui.label_list_shot_thumbnail  # 리스트 뷰 샷 썸네일 레이블 (메타데이터)
        self.label_list_shot_name = self.ui.label_list_shot_name  # 리스트 뷰 샷 이름 레이블 (메타데이터)
        self.label_list_shot_type = self.ui.label_list_shot_type  # 리스트 뷰 샷 타입 레이블 (메타데이터)
        self.label_list_shot_ver = self.ui.label_list_shot_ver  # 리스트 뷰 샷 버전 레이블 (메타데이터)
        self.label_list_shot_link = self.ui.label_list_shot_link  # 리스트 뷰 샷 링크 레이블 (메타데이터)
        self.label_list_shot_date = self.ui.label_list_shot_date    # 리스트 뷰 샷 날짜 레이블 (메타데이터)
        self.label_list_shot_artist = self.ui.label_list_shot_artist    # 리스트 뷰 샷 아티스트 레이블 (메타데이터)
        self.label_list_shot_frame = self.ui.label_list_shot_frame  # 리스트 뷰 샷 프레임 레이블 (메타데이터)
        self.label_list_shot_des = self.ui.label_list_shot_des  # 리스트 뷰 샷 설명 레이블 (메타데이터)
        
        self.label_grid_shot_name = self.ui.label_grid_shot_name    # 어드밴스드 그리드 뷰 샷 이름 레이블 (메타데이터)
        self.label_grid_shot_type = self.ui.label_grid_shot_type    # 어드밴스드 그리드 뷰 샷 타입 레이블 (메타데이터)
        self.label_grid_shot_ver = self.ui.label_grid_shot_ver  # 어드밴스드 그리드 뷰 샷 버전 레이블 (메타데이터)
        self.label_grid_shot_link = self.ui.label_grid_shot_link    # 어드밴스드 그리드 뷰 샷 링크 레이블 (메타데이터)
        self.label_grid_shot_date = self.ui.label_grid_shot_date    # 어드밴스드 그리드 뷰 샷 날짜 레이블 (메타데이터)
        self.label_grid_shot_artist = self.ui.label_grid_shot_artist    # 어드밴스드 그리드 뷰 샷 아티스트 레이블 (메타데이터)
        self.label_grid_shot_frame = self.ui.label_grid_shot_frame  # 어드밴스드 그리드 뷰 샷 프레임 레이블 (메타데이터)
        self.label_grid_shot_des = self.ui.label_grid_shot_des  # 어드밴스드 그리드 뷰 샷 설명 레이블 (메타데이터)
        
        self.tableWidget_grid_full.resizeColumnsToContents()    # 이니셜 그리드 뷰 테이블 위젯 열 너비 자동 조정     
        self.tableWidget_grid_full_pub.resizeColumnsToContents()    # 이니셜 그리드 뷰 테이블 위젯 열 너비 자동 조정        
        self.wip_table.resizeColumnsToContents()    # 어드밴스드 그리드 뷰 테이블 위젯 열 너비 자동 조정
        self.pub_table.resizeColumnsToContents()    # 어드밴스드 그리드 뷰 테이블 위젯 열 너비 자동 조정
        self.wip_list_table.resizeColumnsToContents()    # 리스트 뷰 테이블 위젯 열 너비 자동 조정
        self.pub_list_table.resizeColumnsToContents()    # 리스트 뷰 테이블 위젯 열 너비 자동 조정
        
        self.label_asset = self.ui.label_asset  # 에셋 레이블
        self.label_env = self.ui.label_env  # 환경 레이블
        self.label_mod = self.ui.label_mod  # 모델 레이블
        self.label_seq = self.ui.label_seq  # 시퀀스 레이블
        self.label_shot = self.ui.label_shot    # 샷 레이블
        self.label_ani = self.ui.label_ani  # 애니메이션 레이블????????
        self.stackedWidget_path = self.ui.stackedWidget_path    # 경로 스택 위젯

        self.task_filter_label = QLabel("Showing tasks with status: WIP, Published, Ready to Go")
        self.task_filter_label.setStyleSheet("color: gray; font-style: italic;")
    
        # My Tasks 탭의 레이아웃에 레이블 추가
        tab_layout = self.ui.tab.layout()
        tab_layout.insertWidget(0, self.task_filter_label)
        print("UI 설정 완료.")

    def setup_home_page(self) -> None:
        """홈 페이지 설정 메서드"""
        print("홈 페이지 설정 중...")
        home_widget = QWidget() # 홈 위젯 생성
        main_layout = QVBoxLayout(home_widget)  # 수직 레이아웃 생성
        scroll_area = QScrollArea() # 스크롤 영역 생성
        scroll_widget = QWidget()   # 스크롤 위젯 생성
        self.grid_layout = QGridLayout(scroll_widget)   # 그리드 레이아웃 생성
        scroll_area.setWidget(scroll_widget)    # 스크롤 위젯 설정
        scroll_area.setWidgetResizable(True)    # 스크롤 위젯 크기에 맞게 조정
        main_layout.addWidget(scroll_area)  # 메인 레이아웃에 스크롤 영역 추가
        self.main_stacked_widget.removeWidget(self.main_stacked_widget.widget(0))   # 메인 스택 위젯에서 첫 번째 위젯 제거
        self.main_stacked_widget.insertWidget(0, home_widget)   # 메인 스택 위젯에 홈 위젯 추가
        print("홈 페이지 설정 완료.")


    def setup_connections(self) -> None:
        print("이벤트 연결 설정 중...")
        self.task_tree.itemClicked.connect(self.on_tree_item_clicked)   # Task 트리 아이템 클릭 시 이벤트 연결
        self.asset_tree.itemClicked.connect(self.on_tree_item_clicked)  # Asset 트리 아이템 클릭 시 이벤트 연결
        self.shot_tree.itemClicked.connect(self.on_tree_item_clicked)   # Shot 트리 아이템 클릭 시 이벤트 연결
        
        for table in [self.wip_table, self.pub_table, self.wip_list_table, self.pub_list_table,
                      self.tableWidget_grid_full, self.tableWidget_grid_full_pub]:
            table.cellClicked.connect(self.on_version_item_clicked)     # 버전 테이블 셀 클릭 시 이벤트 연결
        
        self.grid_button.clicked.connect(self.show_initial_grid_view)   # 그리드 뷰 버튼 클릭 시 이벤트 연결
        self.list_button.clicked.connect(self.show_list_view)   # 리스트 뷰 버튼 클릭 시 이벤트 연결
        
        self.home_button.clicked.connect(self.go_home)        # 홈 버튼 클릭 시 이벤트 연결
        
        self.tab_widget.currentChanged.connect(self.test_func) # 탭 변경 시 이벤트 연결
        

        for table in [self.wip_table, self.pub_table, self.wip_list_table, self.pub_list_table, 
                      self.tableWidget_grid_full, self.tableWidget_grid_full_pub]:
            table.cellDoubleClicked.connect(self.on_version_item_double_clicked)    # 버전 테이블 셀 더블 클릭 시 이벤트 연결 ###################################################08/26변경#########################################


        for tab_widget in self.all_viewer_tab_widgets:
            tab_widget.currentChanged.connect(self.on_viewer_tab_clicked)  # 뷰어 탭 위젯 탭 변경 시 이벤트 연결
            
        # pushButton_new_wip로 시작하는 모든 버튼에 대해 이벤트 핸들러를 연결합니다.
        for button_name in dir(self.ui):
            if button_name.startswith('pushButton_new_wip'):
                button = getattr(self.ui, button_name)
                button.clicked.connect(self.on_new_wip_button_clicked) 
  
        self.tasks_search.textChanged.connect(self.start_search_timer)  # 태스크 검색 텍스트 변경 시 이벤트 연결
        self.assets_search.textChanged.connect(self.start_search_timer)  # 에셋 검색 텍스트 변경 시 이벤트 연결
        self.shots_search.textChanged.connect(self.start_search_timer)  # 샷 검색 텍스트 변경 시 이벤트 연결
        self.version_search.textChanged.connect(self.start_search_timer)  # 버전 검색 텍스트 변경 시 이벤트 연결
        print("이벤트 연결 설정 완료.")

    def update_user_name(self) -> None:
        print("사용자 이름 업데이트 중...")
        if hasattr(self, 'user_name_label'):
            self.user_name_label.setText(self.data_explorer.user_info['name'])  # 사용자 이름 레이블에 사용자 이름 설정
            self.setWindowTitle(f"Welcome {self.data_explorer.user_info['name']}")
            
            # step_name = 'Unknown Step' if asset_task.get('step') is None else asset_task['step'].get('name', 'Unknown Step')
            self.user_task = 'Unkknow Step' if self.data_explorer.user_info.get('sg_step') is None else self.data_explorer.user_info['sg_step'].get('name','Not_set')
            # self.user_task = self.data_explorer.user_info.get('sg_step', {}).get('name','Not_set')
            print(f'self.user_task{self.user_task}########@@@@')
            
        print(f"사용자 이름 업데이트 완료: {self.data_explorer.user_info['name']}")

    def go_home(self) -> None:
        print("홈 페이지로 이동 중...")
        # self.current_viewer_tab_index = self.tabWidget_grid_full.currentIndex()  # 현재 선택된 탭 인덱스 저장   
        self.reset_current_path_labels           # 현재 경로 레이블 초기화
        self.reset_tables() # 테이블 초기화
        self.clear_current_project_info            # 현재 프로젝트 정보 초기화
        self.main_stacked_widget.setCurrentIndex(0) # 메인 스택 위젯을 홈 페이지로 설정
        self.load_projects()            # 프로젝트 목록 다시 로드
        self.tabWidget_grid_full.setTabText(0, f"Working")  # 이니셜 그리드 뷰 탭 위젯 Working 탭 이름 설정
        self.tabWidget_grid_full.setTabText(1, f"Publishes")    # 이니셜 그리드 뷰 탭 위젯 Publishes 탭 이름 설정
        self.tableWidget_grid_advanced.setTabText(0, f"Working")  # 어드밴스드 그리드 뷰 탭 위젯 Working 탭 이름 설정
        self.tableWidget_grid_advanced.setTabText(1, f"Publishes")  # 어드밴스드 그리드 뷰 탭 위젯 Publishes 탭 이름 설정
        self.tableWidget_list.setTabText(0, f"Working")     # 리스트 뷰 탭 위젯 Working 탭 이름 설정
        self.tableWidget_list.setTabText(1, f"Publishes")   # 리스트 뷰 탭 위젯 Publishes 탭 이름 설정
        self.show_initial_grid_view()   # 초기 그리드 뷰로 전환
        self.tab_widget.setCurrentIndex(0)  # 탭 위젯을 Tasks 탭으로 설정
        self.second_tab_widget.setCurrentIndex(0)  # 이니셜 그리드 뷰 탭 위젯 Working 탭으로 설정

            
        print("홈 페이지로 이동 완료.")

    def reset_current_path_labels(self) -> None:
        pass

    def reset_tables(self) -> None:
        for table in [self.wip_table, self.pub_table, self.wip_list_table, self.pub_list_table, 
                      self.tableWidget_grid_full, self.tableWidget_grid_full_pub]:
            table.clearContents()
            table.setRowCount(0)
        print("테이블 초기화 완료.")
            # 모든 상태 변수 초기화

    def reset_tables_by_user_task(self) -> None:
        for table in [self.wip_table, self.wip_list_table,
                      self.tableWidget_grid_full]:
            table.clearContents()
            table.setRowCount(0)
        print("테이블 초기화 완료.")
            # 모든 상태 변수 초기화

    def clear_current_project_info(self) -> None:
        self.current_project_id = None
        self.current_project_info = {}
        self.current_entity_type = None
        self.current_view_mode = 'initial_grid_view'
        self.current_task_id = None
        self.current_version_data = None
        self.current_thumbnail_path = None
        self.current_path_info = {}
        self.current_version_info = {}
        self.current_publish_info = {}

        # self.current_viewer_tab_index = 0  # 현재 선택된 탭 인덱스를 저장할 변수

        # UI 요소 초기화
        self.task_tree.clear()
        self.asset_tree.clear()
        self.shot_tree.clear()
        # 경로 레이블 초기화
        self.label_asset.setText("")
        self.label_env.setText("")
        self.label_mod.setText("")
        self.label_seq.setText("")
        self.label_shot.setText("")
        self.label_ani.setText("")
        # 프로젝트 이름 레이블 초기화
        self.project_name_label.setText("")

    def load_projects(self) -> None:
        print("프로젝트 로드 중...")
        projects: List[Dict[str, Any]] = self.data_explorer.get_projects()  # 프로젝트 목록 로드
        print(f"{len(projects)}개의 프로젝트 가져옴.")

        for i in reversed(range(self.grid_layout.count())):     # 홈 그리드 레이아웃에 있는 모든 위젯 제거
            self.grid_layout.itemAt(i).widget().setParent(None)     # 위젯 제거

        for i, project in enumerate(projects):  # 프로젝트 목록을 순회하며
            project_widget = QWidget()  # 프로젝트 위젯 생성
            project_widget.setStyleSheet("background-color: #E6E6FA;")  # 배경색 설정
            project_widget.setFixedSize(285, 285)   # 크기 설정
            project_layout = QVBoxLayout(project_widget)    # 수직 레이아웃 생성

            thumbnail_path = self.thumbnail_manager.download_project_thumbnail(project['id'])   # 썸네일 경로 다운로드
            if thumbnail_path:  # 썸네일 경로가 있을 때
                thumbnail_label = QLabel()  # 썸네일 레이블 생성
                pixmap = QPixmap(thumbnail_path)    # 썸네일 이미지 로드
                sc_pixmap = pixmap.scaledToWidth(285)
                # thumbnail_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # 썸네일 이미지 설정
                thumbnail_label.setPixmap(sc_pixmap)
                project_layout.addWidget(thumbnail_label)   # 썸네일 레이블 추가
                thumbnail_label.setAlignment(Qt.AlignCenter)    # 중앙 정렬 설정


            name_label = QLabel(project['name'])    # 프로젝트 이름 레이블 생성
            name_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)   # 중앙 정렬 설정
            project_layout.addWidget(name_label)    # 이름 레이블 추가

            self.grid_layout.addWidget(project_widget, i // 3, i % 3)   # 그리드 레이아웃에 프로젝트 위젯 추가!!

            project_widget.mousePressEvent = self.create_project_click_handler(project) # 프로젝트 위젯에 클릭 이벤트 핸들러 추가
        
        print("프로젝트 로드 및 표시 완료.")

    def show_initial_grid_view(self) -> None:   # 초기 그리드 뷰로 전환하는 메서드
            print("초기 그리드 뷰로 전환")
            self.stackedWidget_sub.setCurrentIndex(0)   # 서브 스택 위젯을 0번 인덱스로 설정
            self.current_view_mode = 'initial_grid_view'    # 현재 뷰 모드를 초기 그리드 뷰로 설정
    
            self.tabWidget_grid_full.setCurrentIndex(self.current_viewer_tab_index)    # 이니셜 그리드 뷰 탭 위젯을 현재 선택된 탭 인덱스로 설정
            for table in [self.tableWidget_grid_full, self.tableWidget_grid_full_pub]:  # 테이블 위젯을 순회하며
                table.setShowGrid(True) # 그리드 표시 설정
                table.setGridStyle(Qt.SolidLine)    # 그리드 스타일 설정
                table.setStyleSheet("QTableWidget { gridline-color: #d0d0d0; }")    # 테이블 위젯 스타일 설정

    def create_project_click_handler(self, project):    # !!!!!!!!프로젝트 클릭 핸들러 생성!!!!!!!!!
        def handler(event): # 이벤트 핸들러
            self.project_clicked(project['id'], project['name'], project.get('sg_status', ''), project.get('sg_project_resolution_width', ''), project.get('sg_project_resolution_height', ''))
        return handler  # 핸들러 반환

    def project_clicked(self, project_id: int, project_name: str, project_status: str, project_resolution_width, project_resolution_height) -> None:
        print(f"프로젝트 클릭됨: ID = {project_id}, 이름 = {project_name}, 상태 = {project_status}", f"프로젝트 해상도: {project_resolution_width}x{project_resolution_height}")    # 프로젝트 정보 출력
        self.current_project_id = project_id    # 현재 프로젝트 ID 설정
        self.current_project_info = {   # 현재 프로젝트 정보 설정
            'id': project_id,   # ID
            'name': project_name,   # 이름
            'status': project_status,    # 상태
            'project_resolution_width': project_resolution_width,    # 해상도 너비
            'project_resolution_height': project_resolution_height    # 해상도 높이
        }
        self.update_project_details(project_id, project_name, project_status)    # 프로젝트 세부 정보 업데이트
        try:
            self.load_user_tasks()  # 유저 태스크 로드
            self.load_assets()  # 에셋 로드
            self.load_shots()   # 샷 로드
        except Exception as e:
            print(f"데이터 로드 중 오류 발생: {e}")
            self.show_error_message(f"데이터 로드 실패: {str(e)}")  # 새로운 메서드 추가
        self.main_stacked_widget.setCurrentIndex(1)  # 메인 스택 위젯을 프로젝트 페이지로 설정
        self.show_initial_grid_view()   # 초기 그리드 뷰로 전환
        self.print_current_info()   # 현재 정보 출력
        print("프로젝트 클릭 완료.")

    def show_error_message(self, message):
        # 에러 메시지를 UI에 표시하는 로직 구현
        QMessageBox.critical(self, "오류", message)

    def update_project_details(self, project_id: int, project_name: str, project_status: str) -> None:  # 프로젝트 세부 정보 업데이트 메서드
        print(f"프로젝트 세부 정보 업데이트 중: ID = {project_id}, 이름 = {project_name}, 상태 = {project_status}")   # 프로젝트 정보 출력
        if hasattr(self, 'project_name_label'): # 프로젝트 이름 레이블이 있을 때
            self.project_name_label.setText(project_name)   # 프로젝트 이름 레이블에 프로젝트 이름 설정
        print("프로젝트 세부 정보 업데이트 완료.")

    def update_task_tree(self): # 태스크 트리 업데이트 메서드
        """ self.task_groups에 저장된 태스크 정보를 트리 위젯에 표시합니다.? """
        self.task_tree.clear()  # 태스크 트리 초기화
        for entity_type, entities in self.task_groups.items():  # 태스크 그룹을 순회하며
            entity_item = QTreeWidgetItem(self.task_tree, [entity_type])    # 엔티티 아이템 생성(엔티티 타입이 레이블로 표시됨)?
            for entity_name, tasks in entities.items(): # 엔티티 목록을 순회하며
                entity_name_item = QTreeWidgetItem(entity_item, [entity_name])  # 엔티티 이름 아이템 생성(엔티티 이름이 레이블로 표시됨)?
                for task in tasks:  # 태스크 목록을 순회하며
                    task_item = QTreeWidgetItem(entity_name_item, [task['step.Step.code']])#!!!!!!!!!!!!!!!!!!여기가 태스크 마지막 차일드 라벨
                    task_item.setData(0, Qt.UserRole, task['id'])  # 태스크 ID 설정
        self.task_tree.expandAll()  # 태스크 트리 전체 확장

    def _recursive_add_items(self, parent_item, data):  # 재귀적으로 아이템 추가하는 메서드
        if isinstance(data, dict):  # 데이터가 딕셔너리인 경우
            for key, value in data.items(): # 데이터를 순회하며
                child_item = self._create_tree_item(parent_item, key)   # 트리 아이템 생성
                self._recursive_add_items(child_item, value)    # 재귀적으로 아이템 추가
        elif isinstance(data, list):    # 데이터가 리스트인 경우
            for item in data:   # 데이터를 순회하며
                self._create_tree_item(parent_item, self._format_task_item(item))   # 트리 아이템 생성
        elif isinstance(data, tuple):   # 데이터가 튜플인 경우
            for item in data:   # 데이터를 순회하며
                self._create_tree_item(parent_item, self._format_task_item(item))   # 트리 아이템 생성

    def _create_tree_item(self, parent, text):  # 트리 아이템 생성 메서드
        if isinstance(parent, QTreeWidget): # 부모가 QTreeWidget인 경우
            item = QTreeWidgetItem(parent)  # 트리 위젯 아이템 생성
        else:
            item = QTreeWidgetItem()    # 트리 위젯 아이템 생성
            parent.addChild(item)   # 부모에 자식 추가
        item.setText(0, text)   # 텍스트 설정
        return item

    def _format_task_item(self, task):  # 태스크 아이템 format을 바꾸는 메서드
        print(f"######Task: {task}")
        result = f"{task.get('step.Step.code')}"  # 태스크 아이템 포맷 변경
        return result   # 결과 반환

    def load_user_tasks(self):  # 사용자 태스크 로드 메서드
        """ 
        사용자의 태스크를 로드하고 표시합니다. 
        """
        print("사용자 태스크 로드 시작...")
        try:
            tasks = self.data_explorer.get_user_tasks(self.current_project_id)  # 사용자 태스크 로드
            print(f"가져온 태스크 수: {len(tasks)}")    # 가져온 태스크 수 출력
            
            self.task_groups = {
                'Asset': {},
                'Shot': {}
            }   # 태스크 그룹 딕셔너리 생성

            for task in tasks:  # 태스크 목록을 순회하며
                entity = task.get('entity') # 엔티티 가져오기
                if entity:  # 엔티티가 있는 경우
                    entity_type = entity.get('type')    # 엔티티 타입 가져오기
                    entity_name = entity.get('name')    # 엔티티 이름 가져오기
                    if entity_type in self.task_groups: # 엔티티 타입이 태스크 그룹에 있는 경우
                        if entity_name not in self.task_groups[entity_type]:    # 엔티티 이름이 태스크 그룹에 없는 경우
                            self.task_groups[entity_type][entity_name] = []   # 엔티티 이름을 키로 하는 리스트 생성
                            print(f'{task}??????????')
                            print(f'{self.data_explorer.user_info}!!!!!!!!!!!!') 
                            user_info = self.data_explorer.user_info.get('sg_step', {})
                            self.user_task = user_info.get('name','Not_set')
                            if task.get('step.Step.code','N/A') == user_info.get('name','Not_set'):
                                self.task_groups[entity_type][entity_name].append(task)   # 태스크 추가
                else:
                    print(f"Warning: Task {task.get('id')} has no entity information.")

            self.update_task_tree() # 태스크 트리 업데이트
            print("사용자 태스크 로드 및 표시 완료.")
        except Exception as e:
            print(f"태스크 로드 중 오류 발생: {e}")
            QMessageBox.warning(self, "오류", f"태스크 로드 실패: {str(e)}")    

    def load_assets(self) -> None:  # 에셋 로드 메서드
        print("에셋 로드 중...")
        if self.current_project_id is None: # 현재 프로젝트 ID가 없는 경우
            print("선택된 프로젝트가 없습니다. 에셋을 로드할 수 없습니다.")
            return

        assets: List[Dict[str, Any]] = self.data_explorer.get_assets(self.current_project_id)   # 에셋 로드
        asset_tasks: Dict[str, List[Dict[str, Any]]] = self.data_explorer.get_asset_tasks(self.current_project_id)  # 에셋 태스크 로드
        
        print(f"{len(assets)}개의 에셋 가져옴.")    
        self.asset_tree.clear() # 에셋 트리 초기화

        asset_types: Dict[str, List[Dict[str, Any]]] = {}   # 에셋 타입 딕셔너리 생성
        for asset in assets:    # 에셋 목록을 순회하며
            asset_type: str = asset.get('sg_asset_type', '분류되지 않음')   # 에셋 타입 가져오기    
            if asset_type not in asset_types:   # 에셋 타입이 에셋 타입 딕셔너리에 없는 경우
                asset_types[asset_type] = []    # 에셋 타입을 키로 하는 리스트 생성
            asset_types[asset_type].append(asset)   # 에셋 추가 

        for asset_type, assets_list in asset_types.items():   # 에셋 타입과 에셋 목록을 순회하며
            type_item: QTreeWidgetItem = QTreeWidgetItem(self.asset_tree)   # 타입 아이템 생성
            type_item.setText(0, asset_type)    # 타입 아이템 텍스트 설정
            print(f"{asset_type} 유형에 대해 {len(assets_list)}개의 에셋 추가 중")  # 에셋 개수 출력
            for asset in assets_list:   # 에셋 목록을 순회하며
                asset_item: QTreeWidgetItem = QTreeWidgetItem(type_item)    # 에셋 아이템 생성
                asset_item.setText(0, asset['code'])    # 에셋 아이템 텍스트 설정
                asset_item.setData(0, Qt.UserRole, asset['id'])   # 에셋 아이템 데이터 설정

                if asset['code'] in asset_tasks:    # 에셋 코드가 에셋 태스크에 있는 경우
                    added_steps = set() # 추가된 스텝 집합 생성
                    for task in asset_tasks[asset['code']]:   # 에셋 태스크 목록을 순회하며
                        if task['step'] != 'Unknown' and task['step'] not in added_steps:       # 스텝이 Unknown이 아니고 추가된 스텝이 아닌 경우
                            task_item: QTreeWidgetItem = QTreeWidgetItem(asset_item)    # 태스크 아이템 생성
                            task_item.setText(0, task['step'])  # 태스크 아이템 텍스트 설정
                            task_item.setData(0, Qt.UserRole, task['id'])   # 태스크 아이템 데이터 설정
                            added_steps.add(task['step'])   # 스텝 추가

        print("에셋 및 관련 태스크 로드 및 표시 완료.")
    def load_shots(self) -> None:   # 샷 로드 메서드
        print("샷 로드 중...")
        if self.current_project_id is None: # 현재 프로젝트 ID가 없는 경우
            print("선택된 프로젝트가 없습니다. 샷을 로드할 수 없습니다.")   # 에셋을 로드할 수 없다는 메시지 출력
            return

        self.shot_tree.clear()  # 샷 트리 초기화

        sequences: List[Dict[str, Any]] = self.data_explorer.get_sequences(self.current_project_id)  # 시퀀스 로드
        shot_tasks: Dict[str, List[Dict[str, Any]]] = self.data_explorer.get_shot_tasks(self.current_project_id)    # 샷 태스크 로드
        
        print(f"{len(sequences)}개의 시퀀스 가져옴.")

        for sequence in sequences:  # 시퀀스 목록을 순회하며
            sequence_item: QTreeWidgetItem = QTreeWidgetItem(self.shot_tree)    # 시퀀스 아이템 생성
            sequence_item.setText(0, sequence['code'])  # 시퀀스 아이템 텍스트 설정
            sequence_item.setData(0, Qt.UserRole, sequence['id'])   # 시퀀스 아이템 데이터 설정

            shots: List[Dict[str, Any]] = self.data_explorer.get_shots_in_sequence(sequence['id'])  # 시퀀스에 속한 샷 가져오기
            print(f"시퀀스 {sequence['code']}에 대해 {len(shots)}개의 샷 가져옴.")  
            
            for shot in shots:  # 샷 목록을 순회하며
                shot_item: QTreeWidgetItem = QTreeWidgetItem(sequence_item)   # 샷 아이템 생성
                shot_item.setText(0, shot['code'])  # 샷 아이템 텍스트 설정
                shot_item.setData(0, Qt.UserRole, shot['id'])   # 샷 아이템 데이터 설정

                if shot['code'] in shot_tasks:  # 샷 코드가 샷 태스크에 있는 경우
                    for task in shot_tasks[shot['code']]:   # 샷 태스크 목록을 순회하며
                        task_item: QTreeWidgetItem = QTreeWidgetItem(shot_item)  # 태스크 아이템 생성
                        task_item.setText(0, task['step'])  # 태스크 아이템 텍스트 설정
                        task_item.setData(0, Qt.UserRole, task['id'])   # 태스크 아이템 데이터 설정
        print("샷 및 관련 태스크 로드 및 표시 완료.")


    def print_current_info(self):   # 현재 정보 출력 메서드
        print("\n--- Current Information ---")  
        print("Project Info:", self.current_project_info)   # 프로젝트 정보 출력
        print("Path Info:", self.current_path_info) # 경로 정보 출력
        pprint(f"self.current_publish_info: {self.current_publish_info}")   # !!!!!!!!!!!!퍼블리시 정보 출력!!!!!!!!!!!!
        pprint(f"self.current_publish_info: {self.current_version_info}")   # !!!!!!!!!!!!버전 정보 출력!!!!!!!!!!!!
        
        print("\nVersion Info:")
        versions = self.current_version_info.get('versions', [])    # 버전 정보 가져오기
        if not versions:    # 버전 정보가 없는 경우
            print("No version information available")
        for version in versions:    # 버전 목록을 순회하며
            if version is None:
                print("Warning: Encountered None version data")
                continue
            print(f"Version ID: {version.get('id', 'Unknown')}, Name: {version.get('code', 'Unknown')}")    # 버전 ID와 이름 출력
            print(f"  Status: {version.get('sg_status_list', 'Unknown')}")  # 상태 출력
            print(f"  Created At: {version.get('created_at', 'Unknown')}")  # 생성 시간 출력
            print(f"  Updated At: {version.get('updated_at', 'Unknown')}")  # 업데이트 시간 출력
            print(f"  User: {version.get('user', {}).get('name', 'Unknown')}")  # 사용자 출력
            task = version.get('sg_task', {})   # 태스크 정보 가져오기
            print(f"  sg_version_file_type: {version.get('sg_version_file_type', 'unknown')}")  # 버전 파일 타입 출력
            print(f"  Task: {task.get('name', 'Unknown') if task else 'Unknown'}")  # 태스크 이름 출력
            print(f"  Path to Frames: {version.get('sg_path_to_frames', 'Unknown')}")   # 프레임 경로 출력
            print(f"  Description: {version.get('description', 'No description')}") # 설명 출력
            print(f"  sg_path: {version.get('sg_path', 'Unknown')}")    # 경로 출력
            print("---")

        print("\nPublish Info:")
        publishes = self.current_publish_info.get('publishes', [])  # 퍼블리시 정보 가져오기
        if not publishes:   # 퍼블리시 정보가 없는 경우
            print("No publish information available")
        else:
            for publish in publishes:   # 퍼블리시 목록을 순회하며
                if publish is None: # 퍼블리시 정보가 없는 경우
                    print("  Invalid publish data")
                    continue    # 다음으로 넘어감(반복문 계속)
                print(f"Publish ID: {publish.get('id', 'Unknown')}, File Name: {publish.get('code', 'Unknown')}")   # 퍼블리시 ID와 파일 이름 출력
                version = publish.get('version', {})    # 버전 정보 가져오기
                if isinstance(version, dict):   # 버전 정보가 딕셔너리인 경우
                    print(f"  Version: {version.get('name', 'Unknown')}")   # 버전 이름 출력
                else:
                    print(f"  Version: Unknown (Invalid data)")
                print(f"  Created At: {publish.get('created_at', 'Unknown')}")  # 생성 시간 출력
                print(f"  Updated At: {publish.get('updated_at', 'Unknown')}")  # 업데이트 시간 출력
                
                path_info = publish.get('path', {})   # 경로 정보 가져오기
                if isinstance(path_info, dict): # 경로 정보가 딕셔너리인 경우
                    print(f"  Path: {path_info.get('local_path', 'Unknown local path')}")   # 로컬 경로 출력
                else:
                    print(f"  Path: {path_info}")   # 경로 출력
                
                file_type = publish.get('published_file_type', {})  # 퍼블리시 파일 타입 가져오기
                if isinstance(file_type, dict): # 파일 타입이 딕셔너리인 경우
                    print(f"  File Type: {file_type.get('name', 'Unknown')}")   # 파일 타입 출력
                else:
                    print(f"  File Type: Unknown (Invalid data)")
                
                task = publish.get('task', {})  # 태스크 정보 가져오기
                if isinstance(task, dict):  # 태스크 정보가 딕셔너리인 경우
                    print(f"  Task: {task.get('name', 'Unknown')}")  # 태스크 이름 출력
                else:
                    print(f"  Task: Unknown (Invalid data)")
                
                print(f"  Description: {publish.get('description', 'No description')}")  # 설명 출력
                print("---")

        print("---------------------------\n")

###################################################################################################################################
    def on_tree_item_clicked(self, item: QTreeWidgetItem, column: int) -> None: # 트리 아이템 클릭 시 호출되는 메서드
        self.update_path_labels(item)   # 패스 라벨 업데이트
        self.update_current_path_info(item) # 현재 경로 정보 업데이트

        if item.childCount() == 0:  # 최하위 아이템(태스크)인 경우에만 처리
            self.current_task_id = item.data(0, Qt.UserRole)  # 태스크 ID 가져오기
            if self.current_task_id is not None:  # 태스크 ID가 있는 경우
                print(f"Debug - Task ID: {self.current_task_id}")  # 디버그 출력 추가
                self.update_version_and_publish_info(self.current_task_id)  # 버전 및 퍼블리시 정보 업데이트
                self.load_versions(self.current_task_id)        # 버전 로드
            else:
                print("Debug - Task ID is None")  # 디버그 출력 추가

        # 현재 선택된 엔티티 타입 업데이트
        if item.treeWidget() == self.asset_tree:    # 에셋 트리인 경우
            self.current_entity_type = "Asset"  # 현재 엔티티 타입을 에셋으로 설정
        elif item.treeWidget() == self.shot_tree:   # 샷 트리인 경우
            self.current_entity_type = "Shot"   # 현재 엔티티 타입을 샷으로 설정
        elif item.treeWidget() == self.task_tree:   # 태스크 트리인 경우
            path = self.get_item_path(item) # 아이템 경로 가져오기
            if "Asset" in path: # 경로에 Asset이 포함된 경우
                self.current_entity_type = "Asset"
            elif "Shot" in path:
                self.current_entity_type = "Shot"

        if self.user_task not in self.get_item_path(item):
            self.reset_tables_by_user_task()
            print('heyheyheyhey')

        self.print_current_info()

    def update_path_labels(self, item: QTreeWidgetItem):
        # 모든 패스 라벨 초기화
        self.label_asset.setText("")
        self.label_env.setText("")
        self.label_mod.setText("")
        self.label_seq.setText("")
        self.label_shot.setText("")
        self.label_ani.setText("")
        
        path = self.get_item_path(item) # 아이템 경로 가져오기
        print(f"Debug - Path: {path}")
        
        if item.treeWidget() == self.asset_tree:    # 에셋 트리인 경우
            self.stackedWidget_path.setCurrentIndex(1)  # Asset 페이지
            if len(path) > 0:
                self.label_asset.setText(path[0])  
            if len(path) > 1:
                self.label_env.setText(path[1]) 
            if len(path) > 2:
                self.label_mod.setText(path[2])
        elif item.treeWidget() == self.shot_tree or (item.treeWidget() == self.task_tree and path[0] == "Shot"):
            self.stackedWidget_path.setCurrentIndex(2)  # Shot 페이지
            if path[0] == "Shot":
                self.label_seq.setText("Shot")  # 또는 필요에 따라 다른 텍스트로 설정
                if len(path) > 1:
                    self.label_shot.setText(path[1])
                if len(path) > 2:
                    self.label_ani.setText(path[2])
            else:
                if len(path) > 0:
                    self.label_seq.setText(path[0])
                if len(path) > 1:
                    self.label_shot.setText(path[1])
                if len(path) > 2:
                    self.label_ani.setText(path[2])
        elif item.treeWidget() == self.task_tree:
            if "Asset" in path:
                self.stackedWidget_path.setCurrentIndex(1)  # Asset 페이지
                self.label_asset.setText("Asset")
                if len(path) > 1:
                    self.label_env.setText(path[1])
                if len(path) > 2:
                    self.label_mod.setText(path[2])
            elif "Shot" in path:
                self.stackedWidget_path.setCurrentIndex(2)  # Shot 페이지
                self.label_seq.setText("Shot")
                if len(path) > 1:
                    self.label_shot.setText(path[1])
                if len(path) > 2:
                    self.label_ani.setText(path[2])
    def update_current_path_info(self, item: QTreeWidgetItem):  # 현재 경로 정보 업데이트 메서드
        path = self.get_item_path(item) # 아이템 경로 가져오기
        self.current_path_info = {
            'type': item.treeWidget().objectName(), # 트리 위젯 이름
            'path': path    
        }   # 현재 경로 정보 설정

    def get_item_path(self, item: QTreeWidgetItem) -> List[str]:    # 아이템 경로 가져오는 메서드
        path = []
        while item: # 아이템이 있는 동안
            path.insert(0, item.text(0))    # 경로에 아이템 텍스트 추가
            item = item.parent()    # 부모 아이템으로 이동
        return path
    ###################################################################################################################################주석이 원래 코드###################################################################################################################################
    
    def update_version_and_publish_info(self, task_id: int):    # 버전 및 퍼블리시 정보 업데이트 메서드
        print(f"Debug - Updating version and publish info for task ID: {task_id}")
        task = self.data_explorer.sg.find_one("Task", [["id", "is", task_id]], ["entity"])  # 태스크 정보 가져오기
        if not task or not task.get("entity"):  # 태스크가 없거나 엔티티가 없는 경우
            print("Debug - 태스크에 연결된 엔티티를 찾을 수 없습니다.")
            return

        entity = task["entity"] # 엔티티 정보 가져오기
        entity_id = entity["id"]    # 엔티티 ID 가져오기
        entity_type = entity["type"]    # 엔티티 타입 가져오기
        print(f"Debug - Entity info: Type={entity_type}, ID={entity_id}")   

        # 버전 정보 조회
        versions = self.data_explorer.sg.find(
            "Version",  # 버전
            [["entity", "is", {"type": entity_type, "id": entity_id}]],
            ["id", "code", "description", "sg_status_list", "sg_task", "sg_path_to_frames"]
        )   # 버전 정보 가져오기
        print(f"Debug - Found {len(versions)} versions")

        # 퍼블리시 파일에서 정보 조회
        publishes = self.data_explorer.sg.find(
            "PublishedFile",    # 퍼블리시 파일
            [["entity", "is", {"type": entity_type, "id": entity_id}]],
            ["id", "code", "description", "path", "version", "published_file_type", "task"]
        )   # 퍼블리시 정보 가져오기
        print(f"Debug - Found {len(publishes)} published files")

        self.current_version_info = {
            'task_id': task_id,
            'entity_id': entity_id,
            'entity_type': entity_type,
            'versions': versions
        }   # 현재 버전 정보 설정
        self.current_publish_info = {
            'task_id': task_id,
            'entity_id': entity_id,
            'entity_type': entity_type,
            'publishes': publishes
        }   # 현재 퍼블리시 정보 설정

        print("버전 및 퍼블리시 데이터가 업데이트되었습니다.")
        self.print_current_info()   

###################################################################################################################################

    def load_versions(self, task_id: int) -> None:  # 버전 로드 메서드
        print(f"Debug - 태스크 (ID: {task_id})의 버전 로드 중...")
        versions = self.data_explorer.get_version(task_id)          # 버전 정보 가져오기
        print(f'{versions}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        if not isinstance(versions, list):                                  # 버전 정보가 리스트가 아닌 경우
            print(f"Debug - Unexpected versions format: {versions}")        
            return

        wip_versions = []   # WIP 버전 리스트
        pub_versions = []   # Publish 버전 리스트
        self.version_data = versions    # 버전 데이터 설정

        for version in versions:    # 버전 목록을 순회하며
            status = version.get('sg_status_list')  # 상태 가져오기
            if status == 'wip':    # 상태가 WIP인 경우
                wip_versions.append(version)    # WIP 버전 리스트에 추가
            elif status == 'pub':   # 상태가 PUB인 경우
                pub_versions.append(version)    # Publish 버전 리스트에 추가

        print(f"Debug - Found {len(wip_versions)} WIP versions and {len(pub_versions)} PUB versions")
        self.update_all_tablewidgets(wip_versions, pub_versions, task_id)   # 모든 테이블 위젯 업데이트
        print(f"{len(wip_versions)} WIP 버전과 {len(pub_versions)} Publish 버전 로드 완료.")
        self.show_initial_grid_view()   # 초기 그리드 뷰로 전환             

    def update_all_tablewidgets(self, wip_versions: List[Dict[str, Any]], pub_versions: List[Dict[str, Any]], task_id: int) -> None:  # 모든 버전 테이블 업데이트 메서드
        self.update_tablewidget(self.tableWidget_grid_full, wip_versions, "WIP", task_id)  # 이니셜 그리드 뷰 테이블위젯 (Working) 업데이트
        self.update_tablewidget(self.tableWidget_grid_full_pub, pub_versions, "PUB", task_id) # 이니셜 그리드 뷰 테이블위젯 (Punlishes) 업데이트
        self.update_tablewidget(self.wip_table, wip_versions, "WIP", task_id) # 어드벤스드 그리드 뷰 테이블 위젯 (Working) 업데이트
        self.update_tablewidget(self.pub_table, pub_versions, "PUB", task_id) # 어드벤스드 그리드 뷰 테이블 위젯 (Publishes) 업데이트
        self.update_tablewidget(self.wip_list_table, wip_versions, "WIP", task_id)    # 리스트 뷰 테이블 위젯 (Working) 업데이트
        self.update_tablewidget(self.pub_list_table, pub_versions, "PUB", task_id)    # 리스트 뷰 테이블 위젯 (Publishes) 업데이트

        self.tabWidget_grid_full.setTabText(0, f"Working ({len(wip_versions)})")    # 이니셜 그리드 뷰 (Working) 탭 이름 설정(숫자 추가)
        self.tabWidget_grid_full.setTabText(1, f"Publishes ({len(pub_versions)})")  # 이니셜 그리드 뷰 (Publishes) 탭 이름 설정(숫자 추가)
        self.tableWidget_grid_advanced.setTabText(0, f"Working ({len(wip_versions)})")  # 어드밴스드 그리드 뷰 탭 위젯 Working 탭 이름 설정
        self.tableWidget_grid_advanced.setTabText(1, f"Publishes ({len(pub_versions)})")  # 어드밴스드 그리드 뷰 탭 위젯 Publishes 탭 이름 설정
        self.tableWidget_list.setTabText(0, f"Working ({len(wip_versions)})")     # 리스트 뷰 탭 위젯 Working 탭 이름 설정
        self.tableWidget_list.setTabText(1, f"Publishes ({len(pub_versions)})")   # 리스트 뷰 탭 위젯 Publishes 탭 이름 설정

###################################################################################################################################

    def get_sequence_for_shot(self, shot_id: int) -> str:   # 샷의 시퀀스 정보 가져오는 메서드
        shot = self.data_explorer.sg.find_one("Shot", [["id", "is", shot_id]], ["sg_sequence"])   # 샷 정보 가져오기
        if shot and shot.get("sg_sequence"):    # 샷 정보가 있고 시퀀스 정보가 있는 경우
            return shot["sg_sequence"]["name"]  # 시퀀스 이름 반환
        return "Unknown Sequence"   # 알 수 없는 시퀀스 반환

    def update_tablewidget(self, table: QTableWidget, versions: List[Dict[str, Any]], version_type: str, task_id: int) -> None: # 테이블 위젯 업데이트 메서드
        table.clearContents()   # 테이블 위젯 내용 지우기
        
        if table in [self.wip_table, self.pub_table, self.tableWidget_grid_full, self.tableWidget_grid_full_pub]:   # 이니셜 혹은 어드벤스드 그리드 뷰인 경우
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!이니셜 혹은 어드벤스드 그리드 뷰 테이블 위젯 디자인 설정!!!!!!!!
            num_columns = 3
            table.setColumnCount(num_columns)
            
            # 열 너비 계산
            total_width = table.width() # 테이블 전체 너비
            column_width = total_width // num_columns  # 각 열의 너비
            for i in range(num_columns):
                table.setColumnWidth(i, column_width)  # 열 너비 설정
            
            # 행 수 계산
            num_rows = (len(versions) + num_columns - 1) // num_columns  # 데이터에 따라 필요한 행 수
            table.setRowCount(num_rows)  # 행 수 설정
            
            # 데이터 항목을 테이블에 추가
            for index, version in enumerate(versions):
                row = index // num_columns  # 데이터가 들어갈 행 번호
                column = index % num_columns  # 데이터가 들어갈 열 번호
                thumbnail_path = self.thumbnail_manager.download_version_thumbnail(version['id'], version_type.lower())   # 썸네일 경로 가져오기
                version_widget = VersionItemWidget(thumbnail_path, version['code'], True)   # 버전 위젯 생성
                table.setCellWidget(row, column, version_widget)   # 셀 위젯 설정
                table.setRowHeight(row, column_width)    # 행 높이 설정
            
            ################################################################
        
        
        else:   # 리스트 뷰인 경우
            # 리스트 뷰 테이블 위젯 디자인 설정
            table.setRowCount(len(versions))    # 행 수 설정
            table.setColumnCount(2) # 열 수 설정
            
            for index, version in enumerate(versions):  # 버전 목록을 순회하며
                # 썸네일 설정
                thumbnail_path = self.thumbnail_manager.download_version_thumbnail(version['id'], version_type.lower())  # 썸네일 경로 가져오기
                thumbnail_label = QLabel()  # 썸네일 라벨 생성
                if thumbnail_path:  # 썸네일 경로가 있는 경우
                    pixmap = QPixmap(thumbnail_path)    # 썸네일 이미지 가져오기
                    if not pixmap.isNull(): # 썸네일 이미지가 유효한 경우
                        thumbnail_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))   # 썸네일 이미지 설정
                    else:
                        thumbnail_label.setText("Invalid Image")
                else:
                    thumbnail_label.setText("No Image") # 썸네일 이미지가 없는 경우
                table.setCellWidget(index, 0, thumbnail_label)  # 썸네일 라벨 설정
                
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 버전 정보 설정 (버전 코드, 상태, 생성 시간) 이걸 수정하면 보여지는 정보가 바뀜 !!!!!!!!!!!!!!!!!
                version_info = f"{version['code']}\n"   # 버전 코드 설정(이름)
                version_info += f"{version['sg_status_list']}\n"    # 버전 상태 설정
                created_at = self.format_datetime(version.get('created_at', 'N/A?v'))  # 생성 시간 포맷팅
                version_info += f"{created_at}"           # 버전 생성 시간 설정
                
                info_label = QLabel(version_info)   # 정보 라벨 생성
                info_label.setWordWrap(True)    # 줄 바꿈 설정
                table.setCellWidget(index, 1, info_label)   # 셀 위젯 설정
                
                table.setRowHeight(index, 60)   # 행 높이 설정

            table.setColumnWidth(0, 60) # 열 너비 설정
            table.setColumnWidth(1, table.width() - 60)   # 열 너비 설정
###################################################################################################################################
    def format_datetime(self,dt):
        if isinstance(dt, datetime.datetime):
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return dt  # datetime 객체가 아니면 그대로 반환
    def on_version_item_clicked(self, row: int, column: int):
        print("Version item clicked")
        table = self.sender()
        
        try:
            # 현재 활성화된 탭 확인 (Working 또는 Publishes)
            current_tab_index = self.tabWidget_grid_full.currentIndex()
            is_publish_tab = current_tab_index == 1
            version_type = 'pub' if is_publish_tab else 'wip'
            
            # 버전 정보와 썸네일 경로 추출
            if self.current_view_mode == 'list_view':
                version_info = table.cellWidget(row, 1)
                if isinstance(version_info, QLabel):
                    version_code = version_info.text().split('\n')[0]
                thumbnail_label = table.cellWidget(row, 0)
                if isinstance(thumbnail_label, QLabel):
                    self.current_thumbnail_path = thumbnail_label.property("thumbnail_path")
            else:
                version_widget = table.cellWidget(row, column)
                if isinstance(version_widget, VersionItemWidget):
                    version_code = version_widget.version_label.text()
                    self.current_thumbnail_path = version_widget.thumbnail_path
                else:
                    raise ValueError("Expected VersionItemWidget")

            print(f"Loading metadata for version: {version_code}, type: {version_type}")
            
            # 버전 메타데이터 가져오기
            self.current_version_data = self.data_explorer.get_version_metadata(
                self.current_project_id, version_code, version_type
            )
            
            if not self.current_version_data:
                print(f"Warning: Failed to retrieve metadata for version {version_code}")
                return

            # 실제 버전 상태 및 ID 사용
            version_id = self.current_version_data.get('id')

            # 엔티티 타입 결정
            entity = self.current_version_data.get('entity', {})
            entity_type = entity.get('type') if entity else None

            if not entity_type:
                print("Error: Unable to determine entity type")
                return

            print(f"Determined entity type: {entity_type}")

            # 썸네일 경로 찾기
            thumbnail_path = self.find_thumbnail_path(version_type, version_id)

            if thumbnail_path:
                pixmap = QPixmap(thumbnail_path)
                if not pixmap.isNull():
                    if entity_type == 'Shot':
                        self.label_list_shot_thumbnail.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    elif entity_type == 'Asset':
                        self.label_list_asset_thumbnail.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    print(f"Thumbnail set successfully for {entity_type}")
                else:
                    print(f"Error: Invalid thumbnail image at {thumbnail_path}")
            else:
                print("No thumbnail path found")

            # 적절한 핸들러 선택 (Shot 또는 Asset)
            handler = self.shot_handler if entity_type == 'Shot' else self.asset_handler

            # 데이터 업데이트
            if is_publish_tab:
                handler.update_version_pub_details(self.current_version_data)
            else:
                handler.update_version_wip_details(self.current_version_data)
            
            # 현재 엔티티 타입 설정
            self.current_entity_type = entity_type

            # 뷰 모드에 따른 UI 업데이트
            self.update_view_mode()

            print(f"Entity details updated successfully for {entity_type}")

        except Exception as e:
            print(f"Error in on_version_item_clicked: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def find_thumbnail_path(self, version_type: str, version_id: int) -> Optional[str]: # 썸네일 경로 찾는 메서드
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_from_loader','version_thumbnail')   # 썸네일 경로 설정
        type_folder = 'pub' if version_type.lower() == 'pub' else 'wip' # 버전 타입에 따라 폴더 설정
        thumbnail_path = os.path.join(base_path, type_folder, f"version{version_id}_thumbnail.jpg")   # 썸네일 경로 설정
        
        if os.path.exists(thumbnail_path):  # 썸네일 경로가 있는 경우
            return thumbnail_path
        else:
            print(f"Thumbnail not found at: {thumbnail_path}")
            return None
         
    def update_view_mode(self): # 뷰 모드 업데이트 메서드 (리스트 뷰, 어드밴스드 그리드 뷰)
        """Update the UI based on the current view mode."""
        if self.current_view_mode == 'list_view':
            self.stackedWidget_sub.setCurrentIndex(2)  # 리스트 뷰 페이지로 전환
            if self.current_entity_type == 'Asset':
                self.stackedWidget_sub_list.setCurrentIndex(1)  # 에셋 메타데이터 페이지
            else:
                self.stackedWidget_sub_list.setCurrentIndex(0)  # 샷 메타데이터 페이지
        else:
            self.stackedWidget_sub.setCurrentIndex(1)  # 어드벤스드 그리드 뷰 페이지로 전환
            if self.current_entity_type == 'Asset':
                self.stackedWidget_sub_grid.setCurrentIndex(1)  # 에셋 메타데이터 페이지
            else:
                self.stackedWidget_sub_grid.setCurrentIndex(0)  # 샷 메타데이터 페이지

###################################################################################################################################
    def show_advanced_grid_view(self) -> None:  # 고급 그리드 뷰로 전환
            print("고급 그리드 뷰로 전환")
            self.stackedWidget_sub.setCurrentIndex(1)   # advanced_grid_view 페이지로 전환
            self.current_view_mode = 'advanced_grid_view'   # 현재 뷰 모드 설정

            self.second_tab_widget.setCurrentIndex(self.current_viewer_tab_index)  # 뷰어 탭 인덱스 설정
            
            is_shots_tab_open = self.tab_widget.currentIndex() == 2     # 샷 탭이 열려 있는지 확인
            
            if is_shots_tab_open or self.current_entity_type == 'Shot': # 샷 탭이 열려 있거나 현재 엔티티 타입이 샷인 경우
                self.stackedWidget_sub_grid.setCurrentIndex(0)  # 샷 페이지로 전환
            elif self.current_entity_type == 'Asset':   # 현재 엔티티 타입이 에셋인 경우
                self.stackedWidget_sub_grid.setCurrentIndex(1)  # 에셋 페이지로 전환

    def show_list_view(self) -> None:   # 리스트 뷰로 전환
            print("리스트 뷰로 전환")
            self.stackedWidget_sub.setCurrentIndex(2)   # 리스트 뷰 페이지로 전환
            self.current_view_mode = 'list_view'    # 현재 뷰 모드 설정

            self.tableWidget_list.setCurrentIndex(self.current_viewer_tab_index)   # 현재 탭 인덱스 설정
            
            current_tab_index = self.tab_widget.currentIndex()  # 현재 탭 인덱스 가져오기
            if current_tab_index == 1:  # Assets 탭
                self.stackedWidget_sub_list.setCurrentIndex(1)  # 에셋 메타데이터 페이지
            elif current_tab_index == 2:  # Shots 탭
                self.stackedWidget_sub_list.setCurrentIndex(0)  # 샷 메타데이터 페이지
            else:
                self.stackedWidget_sub_list.setCurrentIndex(0)  # 샷 메타데이터 페이지
            
            for table in [self.wip_list_table, self.pub_list_table]:    # 리스트 뷰 테이블 위젯 설정
                table.setShowGrid(False)    # 그리드 숨기기
                table.setStyleSheet("QTableWidget { border: none; }")   # 테이블 위젯 스타일 설정
            
            print(f"Current tab index: {current_tab_index}")
            print(f"stackedWidget_sub_list current index: {self.stackedWidget_sub_list.currentIndex()}")
###################################################################################################################################


    def test_func(self):    # 테스트 함수
        print("Test function called")

    def on_tasks_search_changed(self, text):    # 태스크 검색어 변경 시 호출되는 메서드
        self.filter_tree(self.task_tree, text)  # 태스크 트리 필터링

    def on_assets_search_changed(self, text):   # 에셋 검색어 변경 시 호출되는 메서드
        self.filter_tree(self.asset_tree, text) # 에셋 트리 필터링

    def on_shots_search_changed(self, text):    # 샷 검색어 변경 시 호출되는 메서드
        self.filter_tree(self.shot_tree, text)  # 샷 트리 필터링

    def filter_tree(self, tree: QTreeWidget, text: str) -> None:    
        for i in range(tree.topLevelItemCount()):   # 트리 위젯의 최상위 아이템 수만큼 반복
            item = tree.topLevelItem(i) # 최상위 아이템 가져오기
            self.filter_tree_item(item, text)   # 트리 아이템 필터링

    def filter_versions(self, search_text: str):
        print(f"버전 필터링: {search_text}")
        search_text = search_text.lower()

        table_visible_counts = {
            self.wip_table: 0,
            self.pub_table: 0,
            self.wip_list_table: 0,
            self.pub_list_table: 0,
            self.tableWidget_grid_full: 0,
            self.tableWidget_grid_full_pub: 0
        }

        for table in table_visible_counts.keys():
            is_grid_view = table in [self.wip_table, self.pub_table, self.tableWidget_grid_full, self.tableWidget_grid_full_pub]
            
            for row in range(table.rowCount()):
                should_show = False
                
                if is_grid_view:
                    # Grid view 처리
                    for col in range(table.columnCount()):
                        widget = table.cellWidget(row, col)
                        if isinstance(widget, VersionItemWidget):
                            if search_text in widget.version_label.text().lower():
                                should_show = True
                                break
                else:
                    # List view 처리
                    info_widget = table.cellWidget(row, 1)
                    if isinstance(info_widget, QLabel):
                        if search_text in info_widget.text().lower():
                            should_show = True

                table.setRowHidden(row, not should_show)
                if should_show:
                    table_visible_counts[table] += 1

        print("버전 필터링 완료")
        
    def cleanup_cache(self):    # 캐시 정리
        cache_dirs = [
            os.path.join(self.base_path,'Launcher','Loader','data_from_loader', 'version_thumbnail'),
            os.path.join(self.base_path,'Launcher','Loader', 'data_from_loader','project_thumbnails')
            
        ]

        if not isinstance(cache_dirs, list) or not cache_dirs:
            print("Error: Invalid cache_dirs")
            return
        
        try:
            for cache_dir in cache_dirs:    # 캐시 폴더 순회
                full_path = os.path.abspath(cache_dir)  # 전체 경로 설정
                if os.path.exists(full_path):   # 캐시 폴더가 있는 경우
                    try:
                        for filename in os.listdir(full_path):  # 캐시 폴더 내 파일 순회
                            file_path = os.path.join(full_path, filename)   # 파일 경로 설정
                            if os.path.isfile(file_path):   # 파일인 경우
                                os.unlink(file_path)    # 파일 삭제
                        shutil.rmtree(full_path)    # 캐시 폴더 삭제
                        print(f"{full_path} 폴더가 성공적으로 삭제되었습니다.")
                    except Exception as e:
                        print(f"{full_path} 폴더 삭제 중 오류 발생: {e}")
                else:
                    print(f"{full_path} 폴더가 존재하지 않습니다.")
        except Exception as e:
            print(f"Error clean up local caches: {e}")
            
        self.data_manager_for_saver.clear_cache()
        print('지운다')

    def closeEvent(self, event):    # 종료 이벤트
        self.cleanup_cache()    # 로컬 캐시 정리
        super().closeEvent(event)   # 부모 클래스의 closeEvent 호출
        

###################################################################################################################################

    def on_viewer_tab_clicked(self, index):    # 뷰어 탭 클릭 시 호출되는 메서드
        self.current_viewer_tab_index = index
        # 모든 탭 위젯의 현재 인덱스를 변경
        for tab_widget in self.all_viewer_tab_widgets:
            if tab_widget.currentIndex() != index:
                tab_widget.setCurrentIndex(index)
        
        print(f"Tab changed to index: {index}")


    def on_version_item_double_clicked(self, row: int, column: int):
        print("on_version_item_double_clicked")
        table = self.sender()
        data_need_to_be_save = {}
        
        try:
            current_tab_index = self.tabWidget_grid_full.currentIndex()
            is_publish_tab = current_tab_index == 1
            version_type = 'pub' if is_publish_tab else 'wip'
            
            if self.current_view_mode == 'list_view':
                version_info = table.cellWidget(row, 1)
                if isinstance(version_info, QLabel):
                    version_code = version_info.text().split('\n')[0]
                thumbnail_label = table.cellWidget(row, 0)
                if isinstance(thumbnail_label, QLabel):
                    self.current_thumbnail_path = thumbnail_label.property("thumbnail_path")
            else:
                version_widget = table.cellWidget(row, column)
                if isinstance(version_widget, VersionItemWidget):
                    version_code = version_widget.version_label.text()
                    self.current_thumbnail_path = version_widget.thumbnail_path
                else:
                    raise ValueError("Expected VersionItemWidget")

            print(f"Loading metadata for version: {version_code}, type: {version_type}")
            
            self.current_version_data = self.data_explorer.get_version_metadata(
                self.current_project_id, version_code, version_type
            )
            
            if not self.current_version_data:
                print(f"Warning: Failed to retrieve metadata for version {version_code}")
                return

            version_id = self.current_version_data.get('id')
            entity = self.current_version_data.get('entity', {})
            entity_type = entity.get('type') if entity else None

            if not entity_type:
                print("Error: Unable to determine entity type")
                return

            self.current_entity_type = entity_type

            print(f"Current type: {entity_type}")
            print(self.current_path_info)
            print(f"Version code: {version_code}")
            
            data_need_to_be_save = {
                'email': self.data_explorer.email,
                'user_id': self.data_explorer.user_info.get('id', ''),
                'project_id': self.current_project_id,
                'project_name': self.current_project_info.get('name', ''),
                'project_resolution_width': self.current_project_info.get('project_resolution_width', ''),
                'project_resolution_height': self.current_project_info.get('project_resolution_height', ''),
                'entity_type': self.current_entity_type,
                'task_id': self.current_task_id,
                'version_code': version_code,
                'version_id': version_id,
                'version_type': version_type,
                'task_name': self.current_path_info.get('path', [])[-1] if self.current_path_info.get('path') else '',
                'sequence_name': self.current_path_info.get('path', [])[-2] if len(self.current_path_info.get('path', [])) > 1 else '',
                'path': self.current_version_data.get('sg_path', 'N/A'),
                'file_name': self.current_version_data.get('code', 'N/A')
            }

            if self.current_entity_type == 'Shot':
                shot_data = self.data_explorer.sg.find_one('Shot', [['id', 'is', entity['id']]], ['sg_cut_in', 'sg_cut_out', 'sg_working_duration'])
                print(shot_data)
                if shot_data:
                    data_need_to_be_save.update({
                        'start_frame': shot_data.get('sg_cut_in'),
                        'end_frame': shot_data.get('sg_cut_out'),
                        'duration': shot_data.get('sg_working_duration'),
                    })

            project_data = self.data_explorer.sg.find_one('Project', [['id', 'is', self.current_project_id]], ['sg_fps'])
            if project_data:
                data_need_to_be_save['fps'] = project_data.get('sg_fps')

            print(f"Collected data to save: {data_need_to_be_save}")
            
            self.data_manager_for_saver.save_data_for_saver(data_need_to_be_save)
            print("Data saved successfully")
            print("수집한 정보 로컬에 저장")
            print("vfx 프로그램 실행 준비중...")
            
            sg_path = self.current_version_data.get('sg_path', '')
            if self.current_entity_type == 'Shot':
                handler = self.shot_handler
            else:
                handler = self.asset_handler
                
            if sg_path.lower().endswith('.nk'):
                handler = self.shot_handler
            elif sg_path.lower().endswith('.mb') or sg_path.lower().endswith('.ma'):
                handler = self.asset_handler
            else:
                print(f' error: {sg_path}')

            if is_publish_tab:
                handler.launch_vfx_program_for_pub(self.current_version_data)
                print("Publish 데이터 전달")
            else:
                handler.launch_vfx_program_for_wip(self.current_version_data)
                print("WIP 데이터 전달")

        except Exception as e:
            print(f"Error in on_version_item_double_clicked: {str(e)}")
            traceback.print_exc()

    def on_new_wip_button_clicked(self):    # 새 WIP 버튼 클릭 시 호출되는 메서드
        if self.current_task_id is None:    # 현재 태스크 ID가 없는 경우
            print("Error: No task selected.")
            return

        try:
            # 현재 사용자의 태스크 목록 가져오기
            user_tasks = self.data_explorer.get_user_tasks(self.current_project_id) # 사용자의 태스크 목록 가져오기
            user_task_ids = [task['id'] for task in user_tasks]   # 사용자의 태스크 ID 목록 가져오기

            # 현재 선택된 태스크가 사용자에게 할당된 태스크인지 확인
            if self.current_task_id not in user_task_ids:   # 현재 태스크 ID가 사용자의 태스크 ID 목록에 없는 경우
                print("Error: You can only create new versions for tasks assigned to you.")
                return

            # 현재 태스크 정보 가져오기
            task = self.data_explorer.sg.find_one('Task', [['id', 'is', self.current_task_id]], ['content', 'entity'])  # 현재 태스크 정보 가져오기
            if not task:
                print("Error: Unable to find the selected task.")
                return

            # 새 버전 번호 생성 (코드에서 추출)
            new_version_number = 1

            # 새 버전 코드 생성
            new_version_code = f"{task['content']}_v{new_version_number:03d}"

            # 새 WIP 버전 생성
            new_version = self.data_explorer.sg.create('Version', {
                'project': {'type': 'Project', 'id': self.current_project_id},  # 프로젝트 정보 추가
                'code': new_version_code,   # 새 버전 코드 추가
                'entity': task['entity'],   # 태스크의 엔티티 정보 추가
                'sg_task': {'type': 'Task', 'id': self.current_task_id},    # 태스크 정보 추가
                'sg_status_list': 'wip',
                'user': self.data_explorer.user_info    # 사용자 정보 추가
            })

            print(f"New WIP version created: {new_version_code}")

            # UI 업데이트
            self.update_version_and_publish_info(self.current_task_id)  # 버전 및 퍼블리시 정보 업데이트
            self.load_versions(self.current_task_id)    # 버전 로드

        except Exception as e:
            print(f"Error creating new WIP version: {e}")
                
    def check_user_step_and_current_task(self):   # 사용자 step 및 현재 태스크 확인
        user_step = self.data_explorer.user_info.get('sg_step', {}).get('name', 'N/A')    # 사용자의 step 정보 가져오기
        selected_item = self.current_path_info.get('path', [])  # 현재 선택된 아이템 정보 가져오기
        
        print(f'User step: {user_step}')    
        print(f'Selected item: {selected_item}')
        


    def filter_all_trees(self, search_text: str):
        search_text = search_text.lower()
        
        # Asset 트리 필터링
        self.filter_tree(self.asset_tree, search_text)
        
        # Shot 트리 필터링
        self.filter_tree(self.shot_tree, search_text)
        
        # My Tasks 트리 필터링
        self.filter_tree(self.task_tree, search_text)


    def start_search_timer(self):
        print("검색 타이머 시작")
        self.current_search_widget = self.sender()  # 현재 검색 중인 위젯 설정
        self.search_timer.start(300)   # 300ms 후에 검색 실행
        print(f"타이머 활성 상태: {self.search_timer.isActive()}")

    def perform_search(self):
        print("검색 수행 중...")
        if self.current_search_widget:
            search_text = self.current_search_widget.text().lower()
            print(f"검색어: {search_text}")

            if self.current_search_widget == self.tasks_search:
                self.filter_tree(self.task_tree, search_text)
            elif self.current_search_widget == self.assets_search:
                self.filter_tree(self.asset_tree, search_text)
            elif self.current_search_widget == self.shots_search:
                self.filter_tree(self.shot_tree, search_text)
            elif self.current_search_widget == self.version_search:
                self.filter_versions(search_text)
        else:
            print("현재 검색 중인 위젯이 없습니다.")
        
        print("검색 완료")

    def search_my_tasks_tree(self, search_text: str):   # MY Task 트리 검색
        self.filter_tree(self.task_tree, search_text)   # 트리 필터링

    def search_assets_tree(self, search_text: str):   # 에셋 트리 검색
        self.filter_tree(self.asset_tree, search_text)  # 트리 필터링

    def search_shots_tree(self, search_text: str):  # 샷 트리 검색
        self.filter_tree(self.shot_tree, search_text)   # 트리 필터링

    def filter_tree(self, tree: QTreeWidget, search_text: str):
        # 루트 아이템부터 시작하여 모든 아이템을 재귀적으로 검사
        root = tree.invisibleRootItem()
        self.filter_tree_item(root, search_text)

    def filter_tree_item(self, item: QTreeWidgetItem, search_text: str) -> bool:    # 트리 아이템 필터링
        # 현재 아이템의 텍스트가 검색어를 포함하는지 확인
        item_visible = search_text in item.text(0).lower()  # 아이템의 텍스트가 검색어를 포함하는지 확인
        
        # 자식 아이템들을 검사
        child_count = item.childCount() # 자식 아이템 개수 가져오기
        for i in range(child_count):    # 자식 아이템 순회
            child = item.child(i)   # 자식 아이템 가져오기
            child_visible = self.filter_tree_item(child, search_text)   # 자식 아이템 필터링
            item_visible = item_visible or child_visible    
        
        # 아이템의 가시성 설정
        item.setHidden(not item_visible)    
        
        return item_visible



if __name__ == "__main__":
    print("애플리케이션 시작 중...")
    app: QApplication = QApplication(sys.argv)
    
    if len(sys.argv) > 1:
        email = sys.argv[1]  # 커맨드 라인에서 이메일 주소 받기(로그인 창에서 서브프로세스로 발동시 email 있음 가져옴)
    else:
        print("NO EMAIL INPUT")  
    window: MainWindow = MainWindow(email = email)  # 메인 윈도우 생성
    window.show()
    print("애플리케이션 윈도우 표시됨. 이벤트 루프 시작.")
    
    exit_code = app.exec()
    
    # 프로그램 종료 전 정리 작업
    window.cleanup_cache()
    
    sys.exit(exit_code)

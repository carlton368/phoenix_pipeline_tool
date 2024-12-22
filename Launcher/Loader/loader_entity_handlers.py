import sys
import os
import math
import shutil
import logging
import subprocess
import re
from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit,
    QTableWidget, QTreeWidget, QStackedWidget, QTreeWidgetItem, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QFrame, QHeaderView, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from datetime import datetime
from Launcher.Loader.loader_config_manager import ConfigManager


class AssetHandler():  # 엔티티 데이터를 처리하는 클래스
    """Class to handle asset entity data."""
    def __init__(self, main_window):    
        self.main_window = main_window  # main_window를 가져옴
        self.logger = logging.getLogger(__name__)
        self.config = ConfigManager()   # ConfigManager 인스턴스 생성
        self.base_path = self.config.get_base_path()   
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!label_mapping: label 이름과 label을 매핑하는 딕셔너리!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.label_mapping = {
            'name': ['label_grid_asset_name', 'label_list_asset_name'],
            'type': ['label_grid_asset_type', 'label_list_asset_type'],
            'version': ['label_grid_asset_ver', 'label_list_asset_ver'],
            'link': ['label_grid_asset_link', 'label_list_asset_link'],
            'date': ['label_grid_asset_date', 'label_list_asset_date'],
            'artist': ['label_grid_asset_artist', 'label_list_asset_artist'],
            'description': ['label_grid_asset_des', 'label_list_asset_des']
        }   # label_mapping에는 asset의 정보를 표시할 label 이름이 들어있음

    def update_version_wip_details(self, version_wip_data: Dict[str, Any]) -> None:     # wip 상태인 버전의 메타데이터를 업데이트하는 매서드
        """Update UI with asset version details."""
        try:
            self._update_labels(version_wip_data, is_publish=False) # version data를 이용하여 label을 업데이트
            self.update_thumbnail(self.main_window.current_thumbnail_path)  # thumbnail을 업데이트
            self.logger.info("Asset version details updated successfully")
        except Exception as e:
            self.logger.error(f"Error updating asset version details: {e}")
############################################################################################################
    def update_version_pub_details(self, pub_version_data: Dict[str, Any]) -> None:     # pub 상태인 버전의 메타데이터를 업데이트하는 매서드
        """
        Update UI with asset publish details.
        1번쨰로 메타데이터를 label에 업데이트하기 시작하는 매서드
        """
        try:
            self._update_labels(pub_version_data, is_publish=True)      # publish data를 이용하여 label을 업데이트
            self.update_thumbnail(self.main_window.current_thumbnail_path)  # thumbnail을 업데이트
            self.logger.info("Asset publish details updated successfully")
        except Exception as e:
            self.logger.error(f"Error updating asset publish details: {e}")

    def _update_labels(self, data: Dict[str, Any], is_publish: bool) -> None:   # label을 업데이트하는 매서드
        """Update labels with provided data."""
        for key, label_names in self.label_mapping.items(): # label_mapping에 있는 key와 value를 가져옴
            value = self._get_formatted_value(data, key, is_publish)    # key와 is_publish를 이용하여 value를 가져옴
            for label_name in label_names: # label_names에 있는 label_name을 가져옴
                label = getattr(self.main_window, label_name, None)  # label_name에 해당하는 label을 가져옴
                if label:  # label이 존재하면
                    label.setText(f"{value}") # !!!!!!!!!!!!!!!!!!!!!!!!!!!!label의 text를 업데이트!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!(여기 바꾸면 다 바뀜 str만 인식)
                else:
                    self.logger.warning(f"Label {label_name} not found in main window")
                    
    def get_version_match(self,input_string):   # 버전을 찾는 매서드
        pattern = r"_v\d{3}"    # _v와 숫자 3개로 이루어진 패턴
        match = re.search(pattern, str(input_string))   # input_string에서 패턴을 찾음
        if match:   # 패턴이 존재하면
            matched_part = match.group()    # 패턴에 매칭되는 부분을 가져옴
        print(matched_part)
        if matched_part.startswith('_'): # 문자열이 '_'로 시작하는 경우
            return matched_part[1:]  # 첫 번째 문자('_')를 제외한 나머지 반환
        else:
            return None  # 매칭되지 않았을 경우 None 반환
    
    def process_version(self,data, key : str):  # 버전을 처리하는 매서드
        version_name = str(data.get(key, 'N/A'))    # key에 해당하는 값을 가져옴
        matched_version = self.get_version_match(version_name)  # version_name에서 버전을 찾음
        print(matched_version)
        if matched_version: # 매칭된 버전이 존재하면
            
            return matched_version  # 매칭된 버전 반환
        elif str(version_name).isdigit():   # 숫자로만 이루어진 경우
            # 숫자만 있는 경우 적절한 형식으로 변환
            return f"v{str(version_name).zfill(3)}"  # 3자리로 맞추어 반환
        else:
            return None  # 적절한 버전을 찾지 못한 경우

    def _get_formatted_value(self, data: Dict[str, Any], key: str, is_publish: bool) -> str:    # 포맷된 값을 가져오는 매서드    
        """Get formatted value for a given key."""
        if is_publish:
            return self._get_publish_value(data, key)   # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!is_publish가 True일 경우 publish data에서 값을 가져옴
        else:
            return self._get_version_value(data, key)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!is_publish가 False일 경우 version data에서 값을 가져옴
        
    def _get_publish_value(self, data: Dict[str, Any], key: str) -> str:    # publish data에서 값을 가져오는 매서드
        try:
            """Get value from publish data."""
            if key == 'name':       # 'name': shot의 이름 (code 필드에서 가져옴)  code: shot name
                return data.get('code', 'N/A')  # 'name': shot의 이름 (code 필드에서 가져옴)  code: shot name
            elif key == 'type':         # 'type': shot의 타입 (sg_version_file_type의 name 필드에서 가져옴) sg_version_file_type: version file type
                return data.get('sg_version_file_type', {}).get('name', 'N/A')  # 'type': 올라가있는 파일의 타입 (sg_version_file_type의 name 필드에서 가져옴) sg_version_file_type: version file type
            elif key == 'version': # 'version': shot의 버전 (code 필드에서 가져옴) code: shot version     
                result = self.process_version(data, 'code') # 버전을 처리(이름 수정 및 매칭)
                print(result)
                return result
            elif key == 'link':     # 'link': shot이 연결된 asset (entity의 name 필드에서 가져옴) entity: shot link
                return data.get('entity', {}).get('name', 'N/A')    # 'link': shot이 연결된 asset (entity의 name 필드에서 가져옴) entity: shot link
            elif key == 'date':
                return data.get('created_at', 'N/A')    # 'date': shot이 생성된 날짜 (created_at 필드에서 가져옴) created_at: shot created date
            elif key == 'artist':
                return data.get('user.HumanUser.name', 'N/A') # 'artist': shot을 생성한 아티스트 (created_by의 name 필드에서 가져옴) created_by: shot creator
            elif key == 'frame':
                return data.get('sg_first_frame', 'N/A'), data.get('sg_last_frame', 'N/A')   # 'frame': shot의 프레임 범위 (sg_first_frame, sg_last_frame 필드에서 가져옴) sg_first_frame, sg_last_frame: shot frame range
            elif key == 'description':
                return data.get('description', 'N/A') # 'description': shot의 설명 (description 필드에서 가져옴) description: shot description
            else:
                return 'N/A'
        except:
            print("라벨 업데이트 오류")

    def _get_version_value(self, data: Dict[str, Any], key: str) -> str:
        """Get value from version data."""
        try:
            if key == 'name':
                return data.get('code', 'N/A')  # 'name': shot의 이름 (code 필드에서 가져옴)  code: shot name
            elif key == 'type':
                return data.get('sg_version_file_type', {}).get('name', 'N/A')  # 'type': shot의 타입 (sg_version_file_type의 name 필드에서 가져옴) sg_version_file_type: version file type
            elif key == 'version':
                result = self.process_version(data, 'code') # 버전을 처리(이름 수정 및 매칭)
                print(result)
                return result
            elif key == 'link':
                return data.get('entity', {}).get('name', 'N/A')    # 'link': shot이 연결된 asset (entity의 name 필드에서 가져옴) entity: shot link
            elif key == 'date':
                return data.get('created_at', 'N/A')    # 'date': shot이 생성된 날짜 (created_at 필드에서 가져옴) created_at: shot created date
            elif key == 'artist':
                return data.get('user.HumanUser.name', 'N/A')    # 'artist': shot을 생성한 아티스트 (user의 name 필드에서 가져옴) user: shot creator
            elif key == 'frame':
                return data.get('sg_first_frame', 'N/A'), data.get('sg_last_frame', 'N/A')   # 'frame': shot의 프레임 범위 (sg_first_frame, sg_last_frame 필드에서 가져옴) sg_first_frame, sg_last_frame: shot frame range
            elif key == 'description':
                return data.get('description', 'N/A')   # 'description': shot의 설명 (description 필드에서 가져옴) description: shot description
            else:
                return 'N/A'
        except:
            print("라벨 업데이트 오류")

    def update_thumbnail(self, thumbnail_path: str) -> None:    # thumbnail을 업데이트하는 매서드
        """Update thumbnail for asset in both grid and list views."""
        if thumbnail_path:  # thumbnail_path가 존재하면
            pixmap = QPixmap(thumbnail_path)    # thumbnail_path를 이용하여 pixmap 생성
            if not pixmap.isNull(): # pixmap이 null이 아니면
                # Update grid view thumbnail      그리드 뷰의 메타데이터 표시창에 썸네일 업데이트
                if hasattr(self.main_window, 'label_grid_asset_thumbnail'): # main_window에 label_grid_asset_thumbnail이 존재하면
                    self.main_window.label_grid_asset_thumbnail.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # label_grid_asset_thumbnail에 pixmap를 넣음
                    self.main_window.label_grid_asset_thumbnail.setFixedSize(150, 150)  # label_grid_asset_thumbnail의 크기를 150x150으로 설정
                    self.main_window.label_grid_asset_thumbnail.setAlignment(Qt.AlignCenter)    # label_grid_asset_thumbnail을 가운데 정렬
                
                # Update list view thumbnail    리스트 뷰의 메타데이터 표시창에 썸네일 업데이트
                if hasattr(self.main_window, 'label_list_asset_thumbnail'): # main_window에 label_list_asset_thumbnail이 존재하면
                    self.main_window.label_list_asset_thumbnail.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # label_list_asset_thumbnail에 pixmap를 넣음
                    self.main_window.label_list_asset_thumbnail.setFixedSize(200, 200)  # label_list_asset_thumbnail의 크기를 200x200으로 설정
                    self.main_window.label_list_asset_thumbnail.setAlignment(Qt.AlignCenter)    # label_list_asset_thumbnail을 가운데 정렬
            else:
                self.logger.error("Invalid thumbnail image for asset")
        else:
            self.logger.warning("No thumbnail path available for asset")

    # def set_stacked_widget_index(self):
    #     self.main_window.set_stacked_widget_index(1)  # stacked_widget의 인덱스를 1로 설정

    def launch_vfx_program_for_pub(self, pub_version_data: Dict[str, Any]) -> None:     # pub 상태인 버전의 메타데이터를 이용하여 VFX 프로그램으로 파일을 열기 위한 매서드
        """
        퍼블리쉬 메타데이터를 기반으로 path에 저장된 파일 오픈 (asset 전용)
        """
        try:
            print(pub_version_data)
            self.logger.info("Asset publish details print successfully")
        except Exception as e:
            self.logger.error(f"Error printting pub asset publish details: {e}")
        file_path = pub_version_data.get('sg_path', 'N/A')########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!조회할 패스 필드 여기서 설정!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print(f"file_path : {file_path}!!!!!!!")  
        try:
            if file_path and os.path.exists(file_path) and file_path.lower().endswith(('.mb', '.ma')):
                self.launch_maya_based_on_path(file_path)    # nuke_script_path를 이용하여 누크 실행
                print("마야 런치 시도...wip")
            elif file_path and os.path.exists(file_path) and file_path.lower().endswith(('.nk', '.nknc')):
                self.launch_nuke_based_on_path(file_path)
            else:
                self.launch_maya_based_on_path()
                print("Valid Maya script path not found in ShotGrid or file does not exist. 그냥 열기만 할게")
                
        except Exception as e:    
            self.logger.info("Error open pub asset path, invalid file path: {e}")
            
    def launch_vfx_program_for_wip(self, wip_version_data: Dict[str, Any]) -> None:   # wip 상태인 버전의 메타데이터를 이용하여 VFX 프로그램으로 파일을 열기 위한 매서드
        """wip 버전의 메타데이터를 기반으로 path에 저장된 파일 오픈 (asset 전용)"""
        try:
            print(wip_version_data)
            self.logger.info("Asset wip details print successfully")
        except Exception as e:
            self.logger.error(f"Error printitng wip asset version details: {e}")

        file_path = wip_version_data.get('sg_path', 'N/A')########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!조회할 패스 필드 여기서 설정!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print(f"file_path : {file_path}$%$^D")  
        try:
            if file_path and os.path.exists(file_path) and file_path.lower().endswith(('.mb', '.ma')):
                self.launch_maya_based_on_path(file_path)    # nuke_script_path를 이용하여 누크 실행
                print("마야 런치 시도...wip")
            elif file_path and os.path.exists(file_path) and file_path.lower().endswith(('.nk', '.nknc')):
                self.launch_nuke_based_on_path(file_path)
                print('누크 런치 시도...wip')
            else:
                self.launch_maya_based_on_path()
                print("Valid Maya script path not found in ShotGrid or file does not exist. 그냥 열기만 할게")
                
        except Exception as e:    
            self.logger.info("Error open pub asset path, invalid file path: {e}")

    def launch_maya_based_on_path(self, path=None):
        try:
            maya_scene_path = path  # 파라미터로 받은 path를 maya_scene_path로 설정
            print(f"maya_scene_path : {maya_scene_path}")

            try: 
                maya_executable = self.config.get_value_as_str('Maya', 'executable') # ConfigManager에서 Maya 실행 파일 경로 가져오기 시도
                if not maya_executable: # 가져오지 못한 경우
                    print("Maya executable path가 config.ini에 없습니다.") 
            except Exception as config_error:
                print(f"Nuke 실행 파일 경로를 config.ini에서 가져오지 못 했습니다.: {config_error}")
                maya_executable = '/usr/local/bin/maya' # 설정 파일에서 읽기 실패 시 하드코딩된 경로 사용

            print(f"maya_executable: {maya_executable}")
            
            # 사용자별 Maya 환경 설정 파일 경로
            maya_env_path = f'{self.base_path}/env/maya.env'
            print(f"maya_env_path: {maya_env_path}")

            # 기본 Maya 실행 명령어 구성
            command = f"{maya_executable}"
            print(f"Base command: {command}")
            
            # Maya 환경 파일이 존재하면 source 명령 추가 및 디버깅 echo 추가
            if os.path.exists(maya_env_path):
                command = f"source {maya_env_path} && {command}"
                print(f"환경 파일 확인. Added env file to command: {command}")
            else:
                print(f"환경 파일 없음. Warning: Maya env file {maya_env_path} does not exist and will be skipped.")

            # Maya 스크립트 경로 추가
            if maya_scene_path and os.path.exists(maya_scene_path) and maya_scene_path.lower().endswith(('.mb', '.ma')):
                command += f" {maya_scene_path}"
                print(f"마야 스크립트 확인. Opening Maya scene: {maya_scene_path}")
            else:
                print("Valid Maya scene path not found or file does not exist. Maya will be opened without a script.")

            print(f"최종 커맨드 Final command: {command}")

            # Maya 실행
            subprocess.Popen(command, shell=True, executable='/bin/bash')
            print("Launching Maya with command:", command)

        except Exception as e:
            print(f"마야 런치시 에러 생김 Error launching Maya: {e}")

        except Exception as e:
            print(f"마야 런치시 에러 생김Error launching Maya: {e}")

    def launch_nuke_based_on_path(self, path=None):
        try:
            # nuke_script_path 설정(파라미터로 받은 path사용)
            nuke_script_path = path 
            print(f"nuke_script_path : {nuke_script_path}") 
            try: # ConfigManager에서 Nuke 실행 파일 경로 가져오기 시도
                nuke_executable = self.config.get_value_as_str('Nuke', 'executable')
                if not nuke_executable: # 가져오지 못한 경우
                    print("Nuke executable path가 config.ini에 없습니다.")    
            except Exception as config_error:
                print(f"Nuke 실행 파일 경로를 config.ini에서 가져오지 못 했습니다.: {config_error}")
                nuke_executable = '/opt/nuke/project/Nuke15.1v1/Nuke15.1' # 설정 파일에서 읽기 실패 시 하드코딩된 경로 사용
            print(f"nuke_executable: {nuke_executable}")
            
            # 사용자별 Nuke 환경 설정 파일 경로 self.base_path = self.config.get_base_path()
            nuke_env_path = f'{self.base_path}/env/nuke.env'
            print(f"nuke_env_path: {nuke_env_path}")    

            # 기본 Nukex 실행 명령어 구성
            command = f"{nuke_executable} --nukex"
            print(f"Base command: {command}")
                
            # Nuke 환경 파일이 실재로 존재하면 source 명령 추가
            if os.path.exists(nuke_env_path):
                command = f"source {nuke_env_path} && {command}"
                print(f"환경 파일 확인. Added env file to command: {command}")
            else:
                print(f"환경 파일 없음. Warning: Nuke env file {nuke_env_path} does not exist and will be skipped.")

            # Nuke 스크립트 경로 추가
            if nuke_script_path and os.path.exists(nuke_script_path) and nuke_script_path.lower().endswith(('.nk', '.nknc')):
                command += f" {nuke_script_path}"
                print(f"뉴크 스크립트 확인. Opening Nuke script: {nuke_script_path}")
            else:
                print("뉴크 스크립트 없음. Valid Nuke script path not found or file does not exist. Nuke will be opened without a script.")

            print(f"최종 커맨드: {command}")

            # Nuke 실행
            subprocess.Popen(command, shell=True, executable='/bin/bash')
            print("Launching Nuke with command:", command)

        except Exception as e:
            print(f"Error launching Nuke: {e}")
############################################################################################################################################################################
############################################################################################################################################################################


class ShotHandler():   # shot의 데이터를 처리하는 클래스
    """Class to handle shot entity data."""
    def __init__(self, main_window):
        self.main_window = main_window  # main_window를 가져옴
        self.logger = logging.getLogger(__name__)
        self.config = ConfigManager()   # ConfigManager 인스턴스 생성
        self.base_path = self.config.get_base_path()
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!label_mapping: label 이름과 label을 매핑하는 딕셔너리!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.label_mapping = {
            'name': ['label_grid_shot_name', 'label_list_shot_name'],
            'type': ['label_grid_shot_type', 'label_list_shot_type'],
            'version': ['label_grid_shot_ver', 'label_list_shot_ver'],
            'link': ['label_grid_shot_link', 'label_list_shot_link'],
            'date': ['label_grid_shot_date', 'label_list_shot_date'],
            'artist': ['label_grid_shot_artist', 'label_list_shot_artist'],
            'frame': ['label_grid_shot_frame', 'label_list_shot_frame'],
            'description': ['label_grid_shot_des', 'label_list_shot_des']
        }   # label_mapping에는 shot의 정보를 표시할 label 이름이 들어있음

    def update_version_wip_details(self, version_data):  # wip 상태인 버전의 메타데이터를 업데이트하는 매서드
        """Update UI with asset version details."""
        try:
            self._update_labels(version_data, is_publish=False) # version data를 이용하여 label을 업데이트
            self.update_thumbnail(self.main_window.current_thumbnail_path)  # thumbnail을 업데이트
            self.logger.info("shot version details updated successfully")
        except Exception as e:
            self.logger.error(f"Error updating shot version details: {e}")
############################################################################################################################################################################
    def update_version_pub_details(self, publish_data: Dict[str, Any]) -> None:     # pub 상태인 버전의 메타데이터를 업데이트하는 매서드
        """
        Update UI with shot publish details.
        1번쨰로 메타데이터를 label에 업데이트하기 시작하는 매서드
        """
        try:
            self._update_labels(publish_data, is_publish=True)      # publish data를 이용하여 label을 업데이트
            self.update_thumbnail(self.main_window.current_thumbnail_path)  # thumbnail을 업데이트
            self.logger.info("shot publish details updated successfully")
        except Exception as e:
            self.logger.error(f"Error updating shot publish details: {e}")

    def _update_labels(self, data: Dict[str, Any], is_publish: bool) -> None:   # label을 업데이트하는 매서드
        """Update labels with provided data."""
        for key, label_names in self.label_mapping.items(): # label_mapping에 있는 key와 value를 가져옴
            value = self._get_formatted_value(data, key, is_publish)    # key와 is_publish를 이용하여 value를 가져옴
            for label_name in label_names: # label_names에 있는 label_name을 가져옴
                label = getattr(self.main_window, label_name, None)  # label_name에 해당하는 label을 가져옴
                if label:  # label이 존재하면
                    label.setText(f"{value}") # !!!!!!!!!!!!!!!!!!!!!!!!!!!!label의 text를 업데이트!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!(여기 바꾸면 다 바뀜 str만 인식)
                else:
                    self.logger.warning(f"Label {label_name} not found in main window")

    def _get_formatted_value(self, data: Dict[str, Any], key: str, is_publish: bool) -> str:    # 형식을 바꿔서 값을 가져오는 매서드 
        """Get formatted value for a given key."""
        if is_publish:
            return self._get_publish_value(data, key)   # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!is_publish가 True일 경우 publish data에서 값을 가져옴
        else:
            return self._get_version_value(data, key)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!is_publish가 False일 경우 version data에서 값을 가져옴
        
    def get_version_match(self,input_string):   # 버전을 찾는 매서드
        pattern = r"_v\d{3}"    # _v와 숫자 3개로 이루어진 패턴
        match = re.search(pattern, str(input_string))   # input_string에서 패턴을 찾음
        if match:   # 패턴이 존재하면
            matched_part = match.group()    # 패턴에 매칭되는 부분을 가져옴
        print(matched_part)
        if matched_part.startswith('_'): # 문자열이 '_'로 시작하는 경우
            return matched_part[1:]  # 첫 번째 문자('_')를 제외한 나머지 반환
        else:
            return None  # 매칭되지 않았을 경우 None 반환
    
    def process_version(self,data, key : str):  # 버전을 처리하는 매서드
        if not data:    # 데이터가 없는 경우
            data = {}   # 빈 데이터로 설정
        version_name = str(data.get(key, 'N/A'))    # key에 해당하는 값을 가져옴
        matched_version = self.get_version_match(version_name)  # version_name에서 버전을 찾음
        print(matched_version)  
        if matched_version: # 매칭된 버전이 존재하면
            
            return matched_version  # 매칭된 버전 반환
        elif str(version_name).isdigit():   
            # 숫자만 있는 경우 적절한 형식으로 변환
            return f"v{str(version_name).zfill(3)}" # 3자리로 맞추어 반환
        else:
            return None  # 적절한 버전을 찾지 못한 경우
        
    def _get_publish_value(self, data: Dict[str, Any], key: str) -> str:   
        """Get value from publish data."""
        try:
            if key == 'name':   
                return data.get('code', 'N/A')  # 'name': shot의 이름 (code 필드에서 가져옴)  code: shot name 
            elif key == 'type':     
                return data.get('sg_version_file_type', {}).get('name', 'N/A') 
            elif key == 'version':
                result = self.process_version(data, 'code') # 버전을 처리(이름 수정 및 매칭)
                print(result)
                return result
            elif key == 'link': 
                return data.get('entity', {}).get('name', 'N/A')    
            elif key == 'date':
                return data.get('created_at', 'N/A')    # 'date': shot이 생성된 날짜 (created_at 필드에서 가져옴) created_at: shot created date
            elif key == 'artist':
                return data.get('user.HumanUser.name', 'N/A') # 'artist': shot을 생성한 아티스트 (created_by의 name 필드에서 가져옴) created_by: shot creator
            elif key == 'frame':
                return data.get('sg_first_frame', 'N/A'), data.get('sg_last_frame', 'N/A')   # 'frame': shot의 프레임 범위 (sg_first_frame, sg_last_frame 필드에서 가져옴) sg_first_frame, sg_last_frame: shot frame range
            elif key == 'description':
                return data.get('description', 'N/A') # 'description': shot의 설명 (description 필드에서 가져옴) description: shot description
            else:
                return 'N/A'
        except:
            print("라벨 업데이트 오류")

    def _get_version_value(self, data: Dict[str, Any], key: str) -> str:    # 버전 값을 가져오는 매서드
        """Get value from version data."""
        try:
            if key == 'name':
                return data.get('code', 'N/A')  # 'name': shot의 이름 (code 필드에서 가져옴)  code: shot name
            elif key == 'type':
                return data.get('sg_version_file_type', {}).get('name', 'N/A')  # 'type': 올라가있는 파일의 타입 (sg_version_file_type의 name 필드에서 가져옴) sg_version_file_type: version file type
            elif key == 'version':
                result = self.process_version(data, 'code') # 버전을 처리(이름 수정 및 매칭)
                print(result)
                return result
            elif key == 'link':     # 'link': shot이 연결된 asset (entity의 name 필드에서 가져옴) entity: shot link
                return data.get('entity', {}).get('name', 'N/A')    # 'link': shot이 연결된 asset (entity의 name 필드에서 가져옴) entity: shot link
            elif key == 'date':
                return data.get('created_at', 'N/A')    # 'date': shot이 생성된 날짜 (created_at 필드에서 가져옴) created_at: shot created date
            elif key == 'artist':
                return data.get('user.HumanUser.name', 'N/A')  # 'artist': shot을 생성한 아티스트 (user의 name 필드에서 가져옴) user: shot creator
            elif key == 'frame':
                return data.get('sg_first_frame', 'N/A'), data.get('sg_last_frame', 'N/A')   # 'frame': shot의 프레임 범위 (sg_first_frame, sg_last_frame 필드에서 가져옴) sg_first_frame, sg_last_frame: shot frame range
            elif key == 'description':
                return data.get('description', 'N/A')   # 'description': shot의 설명 (description 필드에서 가져옴) description: shot description
            else:
                return 'N/A'
        except:
            print("라벨 업데이트 오류")

    def update_thumbnail(self, thumbnail_path: str) -> None:    # thumbnail을 업데이트하는 매서드
        """Update thumbnail for shot in both grid and list views."""
        if thumbnail_path:  # thumbnail_path가 존재하면
            pixmap = QPixmap(thumbnail_path)    # thumbnail_path를 이용하여 pixmap 생성
            if not pixmap.isNull(): # pixmap이 null이 아니면
                # Update grid view thumbnail      그리드 뷰의 메타데이터 표시창에 썸네일 업데이트
                if hasattr(self.main_window, 'label_grid_shot_thumbnail'): # main_window에 label_grid_shot_thumbnail이 존재하면
                    self.main_window.label_grid_shot_thumbnail.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # label_grid_shot_thumbnail에 pixmap를 넣음
                    self.main_window.label_grid_shot_thumbnail.setFixedSize(150, 150)  # label_grid_shot_thumbnail의 크기를 150x150으로 설정
                    self.main_window.label_grid_shot_thumbnail.setAlignment(Qt.AlignCenter)    # label_grid_shot_thumbnail을 가운데 정렬
                
                # Update list view thumbnail    리스트 뷰의 메타데이터 표시창에 썸네일 업데이트
                if hasattr(self.main_window, 'label_list_shot_thumbnail'): # main_window에 label_list_shot_thumbnail이 존재하면
                    self.main_window.label_list_shot_thumbnail.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # label_list_shot_thumbnail에 pixmap를 넣음
                    self.main_window.label_list_shot_thumbnail.setFixedSize(200, 200)  # label_list_shot_thumbnail의 크기를 200x200으로 설정
                    self.main_window.label_list_shot_thumbnail.setAlignment(Qt.AlignCenter)    # label_list_shot_thumbnail을 가운데 정렬
            else:
                self.logger.error("Invalid thumbnail image for shot")
        else:
            self.logger.warning("No thumbnail path available for shot")
################################################################################################08/26################################################################# 

    def launch_vfx_program_for_pub(self, pub_version_data: Dict[str, Any]) -> None:     # pub 상태인 버전의 메타데이터를 이용하여 VFX 프로그램으로 파일을 열기 위한 매서드
        """
        퍼블리쉬 메타데이터를 기반으로 path에 저장된 파일 오픈 (shot 전용)
        """
        try:
            print(pub_version_data)   # pub_version_data 출력
            self.logger.info("shot publish details print successfully")
        except Exception as e:
            self.logger.error(f"Error printting pub shot publish details: {e}")
            
        file_path = pub_version_data.get('sg_path', 'N/A')########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!조회할 패스 필드 여기서 설정!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print(f"file_path : {file_path}")
        try:
            if file_path and os.path.exists(file_path) and file_path.lower().endswith(('.nk', '.nknc')):
                self.launch_nuke_based_on_path(file_path) # nuke_script_path를 이용하여 누크 실행
            elif file_path and os.path.exists(file_path) and file_path.lower().endswith(('.mb', '.ma')):
                self.launch_maya_based_on_path(file_path)    # mayapath를 이용하여 누크 실행
                print("마야 런치 시도...wip")
            else:
                self.launch_nuke_based_on_path()
                print("Valid Nuke script path not found in ShotGrid or file does not exist. 그냥 열기만 할게")
                
        except Exception as e:    
            self.logger.info("Error open pub shot path, invalid file path: {e}")
            
    def launch_vfx_program_for_wip(self, wip_version_data: Dict[str, Any]) -> None:
        """wip 버전의 메타데이터를 기반으로 path에 저장된 파일 오픈 (shot 전용)"""
        try:
            print(wip_version_data)
            self.logger.info("shot publish details print successfully") 
        except Exception as e:
            self.logger.error(f"Error printting pub shot publish details: {e}")
            
        file_path = wip_version_data.get('sg_path', 'N/A')########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!조회할 패스 필드 여기서 설정!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print(f"file_path : {file_path}")
        try:
            if file_path and os.path.exists(file_path) and file_path.lower().endswith(('.nk', '.nknc')):
                self.launch_nuke_based_on_path(file_path) # nuke_script_path를 이용하여 누크 실행
            elif file_path and os.path.exists(file_path) and file_path.lower().endswith(('.mb', '.ma')):
                self.launch_maya_based_on_path(file_path)    # mayapath를 이용하여 누크 실행
                print("마야 런치 시도...wip")
            else:
                self.launch_nuke_based_on_path()
                print("Valid Nuke script path not found in ShotGrid or file does not exist. 그냥 열기만 할게")
                
        except Exception as e:    
            self.logger.info("Error open pub shot path, invalid file path: {e}")

############################################################################################################################################################################
    def launch_maya_based_on_path(self, path=None):
        try:
            maya_scene_path = path  # 파라미터로 받은 path를 maya_scene_path로 설정
            print(f"maya_scene_path : {maya_scene_path}")

            try: 
                maya_executable = self.config.get_value_as_str('Maya', 'executable') # ConfigManager에서 Maya 실행 파일 경로 가져오기 시도
                if not maya_executable: # 가져오지 못한 경우
                    print("Maya executable path가 config.ini에 없습니다.") 
            except Exception as config_error:
                print(f"Nuke 실행 파일 경로를 config.ini에서 가져오지 못 했습니다.: {config_error}")
                maya_executable = '/usr/local/bin/maya' # 설정 파일에서 읽기 실패 시 하드코딩된 경로 사용

            print(f"maya_executable: {maya_executable}")
            
            # 사용자별 Maya 환경 설정 파일 경로
            maya_env_path = f'{self.base_path}/env/maya.env'
            print(f"maya_env_path: {maya_env_path}")

            # 기본 Maya 실행 명령어 구성
            command = f"{maya_executable}"
            print(f"Base command: {command}")
            
            # Maya 환경 파일이 존재하면 source 명령 추가 및 디버깅 echo 추가
            if os.path.exists(maya_env_path):
                command = f"source {maya_env_path} && {command}"
                print(f"환경 파일 확인. Added env file to command: {command}")
            else:
                print(f"환경 파일 없음. Warning: Maya env file {maya_env_path} does not exist and will be skipped.")

            # Maya 스크립트 경로 추가
            if maya_scene_path and os.path.exists(maya_scene_path) and maya_scene_path.lower().endswith(('.mb', '.ma')):
                command += f" {maya_scene_path}"
                print(f"마야 스크립트 확인. Opening Maya scene: {maya_scene_path}")
            else:
                print("Valid Maya scene path not found or file does not exist. Maya will be opened without a script.")

            print(f"최종 커맨드 Final command: {command}")

            # Maya 실행
            subprocess.Popen(command, shell=True, executable='/bin/bash')
            print("Launching Maya with command:", command)

        except Exception as e:
            print(f"마야 런치시 에러 생김 Error launching Maya: {e}")

    def launch_nuke_based_on_path(self, path=None):
        try:
            # nuke_script_path 설정(파라미터로 받은 path사용)
            nuke_script_path = path 
            print(f"nuke_script_path : {nuke_script_path}") 
            try: # ConfigManager에서 Nuke 실행 파일 경로 가져오기 시도
                nuke_executable = self.config.get_value_as_str('Nuke', 'executable')
                if not nuke_executable: # 가져오지 못한 경우
                    print("Nuke executable path가 config.ini에 없습니다.")    
            except Exception as config_error:
                print(f"Nuke 실행 파일 경로를 config.ini에서 가져오지 못 했습니다.: {config_error}")
                nuke_executable = '/opt/nuke/project/Nuke15.1v1/Nuke15.1' # 설정 파일에서 읽기 실패 시 하드코딩된 경로 사용
            print(f"nuke_executable: {nuke_executable}")

            # 사용자별 Nuke 환경 설정 파일 경로 self.base_path = self.config.get_base_path()
            nuke_env_path = f'{self.base_path}/env/nuke.env'
            print(f"nuke_env_path: {nuke_env_path}")    

            # 기본 Nukex 실행 명령어 구성
            command = f"{nuke_executable} --nukex"
            print(f"Base command: {command}")
                
            # Nuke 환경 파일이 실재로 존재하면 source 명령 추가
            if os.path.exists(nuke_env_path):
                command = f"source {nuke_env_path} && {command}"
                print(f"환경 파일 확인. Added env file to command: {command}")
            else:
                print(f"환경 파일 없음. Warning: Nuke env file {nuke_env_path} does not exist and will be skipped.")

            # Nuke 스크립트 경로 추가
            if nuke_script_path and os.path.exists(nuke_script_path) and nuke_script_path.lower().endswith(('.nk', '.nknc')):
                command += f" {nuke_script_path}"
                print(f"뉴크 스크립트 확인. Opening Nuke script: {nuke_script_path}")
            else:
                print("뉴크 스크립트 없음. Valid Nuke script path not found or file does not exist. Nuke will be opened without a script.")

            print(f"최종 커맨드: {command}")

            # Nuke 실행
            subprocess.Popen(command, shell=True, executable='/bin/bash')
            print("Launching Nuke with command:", command)

        except Exception as e:
            print(f"Error launching Nuke: {e}")

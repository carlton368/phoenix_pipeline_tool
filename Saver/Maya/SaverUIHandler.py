import sys
sys.path.append('/home/rapa/_phoenix_/lib/site-packages')

try:
    from PySide6.QtWidgets import *
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Qt, QTimer
    from PySide6.QtCore import QPoint
    from PySide6.QtGui import QPixmap, QFont, QMovie
    from PySide6.QtGui import QGuiApplication
except:
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Qt, QTimer
    from PySide2.QtCore import QPoint
    from PySide2.QtGui import QPixmap, QFont, QMovie
    from PySide2.QtGui import QGuiApplication

import os
import re
import json
import threading
from functools import partial
from Saver.Maya.file_saver import FileSaver
from Saver.Maya.data_explorer_json import DataExplorerJson
from ui.ui_saver import Ui_Form

"""
어떤 프로그램에서 모듈이 실행되는지 확인
"""
try:
    import maya.cmds as cmds  
    from Saver.Maya.get_maya_path import MayaCurrentPathImporter
    current_path_importer = MayaCurrentPathImporter()
    current_path = current_path_importer.show_file_path()
    in_maya = True
except ImportError:
    in_maya = False

class ShotgridWorker(threading.Thread):
    """
    로딩 페이지를 띄울때 동시에 JSON파일을 받는 클래스입니다.
    """
    
    def __init__(self, project_id, user_id):
        super().__init__()
        self.explorer_json = DataExplorerJson()
        self.project_id = project_id
        self.user_id = user_id
        self._stop_event = threading.Event()
        self._on_task_finished = None

    def run(self):
        try:
            while not self._stop_event.is_set():
                # 데이터를 가져와 JSON 파일로 저장하는 작업을 수행합니다.
                print("Starting JSON export...")
                self.explorer_json.make_project_user_json(self.project_id, self.user_id)
                print("Project user JSON created.")
                self.explorer_json.make_assets_json(self.project_id)
                print("Assets JSON created.")
                self.explorer_json.make_shots_json(self.project_id)
                print("Shots JSON created.")
                self.explorer_json.make_user_assigned_work_json(self.project_id, self.user_id)
                print("User assigned work JSON created.")

                # 작업 완료 시그널을 발생시킵니다.
                if self._on_task_finished:
                    # 콜백을 UI 스레드의 이벤트 루프 끝에 예약함으로써 스레드가 안전하게 UI를 업데이트할 수 있도록 합니다.
                    QTimer.singleShot(0, self._on_task_finished) 
                self.on_task_finished()
                self._stop_event.set()
                print('-------------------------------------------')
                
        except Exception as e:
            print(f"Error in thread: {e}")
    
    def stop(self):
        """스레드를 안전하게 종료합니다."""
        self._stop_event.set()  # 스레드 종료 신호
        self.join()  # 스레드가 종료될 때까지 대기합니다.
        
    @property    
    def on_task_finished(self):
        return self._on_task_finished
    
    @on_task_finished.setter
    def on_task_finished(self, callback):
        self._on_task_finished = callback

class SaverUIHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.setting()
        self.setWindowTitle("Phoenix Save")
        self.find_root_path()
        self.initial_path = current_path
        self.explorer_json = DataExplorerJson()
        self.project_json_path = f'{self.root_path}/_phoenix_/Saver/project_json'
        self.connect_signals()
        self.first_show()
        
        # 원래 stdout을 저장합니다.
        self.original_stdout = sys.stdout
        
        # Json파일을 로딩할때 gif 페이지를 보여줍니다.
        self.show_loading_page()
        
        self.setup_search_mode()
        
        
    """
    이벤트 함수 모음
    """
    def connect_signals(self):   # 시그널들 모음
        self.ui.tabWidget_pathtree.currentChanged.connect(self.event_tree_tab_changed)
        select_btn_list = ["shots_all","shots_none","assets_all","assets_none"]
        for i in select_btn_list:
            getattr(self.ui,f"pushButton_{i}").clicked.connect(partial(self.event_select_btn,i))
        self.ui.checkBox_avaliable_ver.stateChanged.connect(self.set_new_file_ver)
        self.ui.checkBox_avaliable_path.stateChanged.connect(self.select_path)
        self.ui.pushButton_cancel.clicked.connect(self.close_ui)
        self.ui.pushButton_save.clicked.connect(self.save_file)
        self.ui.treeWidget_my_tasks.currentItemChanged.connect(self.show_my_tasks_data)
        self.ui.treeWidget_assets.currentItemChanged.connect(self.show_asset_file_data)
        self.ui.treeWidget_shots.currentItemChanged.connect(self.show_shot_file_data)
        self.ui.spinBox_version.valueChanged.connect(self.event_save_info_changed)
        self.ui.comboBox_filetype.currentIndexChanged.connect(self.event_save_info_changed)
        
        # Search창 텍스트 변경시 이벤트 연결
        self.ui.lineEdit_search_my_tasks.textChanged.connect(self.start_search_timer) 
        self.ui.lineEdit_search_assets.textChanged.connect(self.start_search_timer)  
        self.ui.lineEdit_search_shots.textChanged.connect(self.start_search_timer) 
        self.ui.lineEdit_search_all.textChanged.connect(self.start_search_timer)  
        self.ui.lineEdit_search_wip.textChanged.connect(self.start_search_timer)  
        self.ui.lineEdit_search_pub.textChanged.connect(self.start_search_timer)  
        
        # Filter 체크박스 상태 변경시 이벤트 연결
        self.ui.checkBox_mod.stateChanged.connect(self.filter_tree_by_checkboxes)
        self.ui.checkBox_rig.stateChanged.connect(self.filter_tree_by_checkboxes)
        self.ui.checkBox_lkd.stateChanged.connect(self.filter_tree_by_checkboxes)
        
        self.ui.checkBox_ani.stateChanged.connect(self.filter_tree_by_checkboxes)
        self.ui.checkBox_lgt.stateChanged.connect(self.filter_tree_by_checkboxes)
        self.ui.checkBox_cmp.stateChanged.connect(self.filter_tree_by_checkboxes)
        self.ui.checkBox_mm.stateChanged.connect(self.filter_tree_by_checkboxes)
        self.ui.checkBox_ly.stateChanged.connect(self.filter_tree_by_checkboxes)
        self.ui.checkBox_fx.stateChanged.connect(self.filter_tree_by_checkboxes)
        
    def show_my_tasks_data(self):    # my task 폴더트리 선택시 실행되는 함수들
        if not self.ui.checkBox_avaliable_path.isChecked():
            self.change_current_path('my_task_signal')
        self.change_my_tasks_path()
        self.set_all_table_list('my_task_signal')
        self.set_file_table_list('my_task_signal')
    
    def show_asset_file_data(self):     # asset 폴더트리 선택시 실행되는 함수들
        if not self.ui.checkBox_avaliable_path.isChecked():
            self.change_current_path('asset_signal')
        self.change_asset_path()
        self.set_all_table_list('asset_signal')
        self.set_file_table_list('asset_signal')
    
    def show_shot_file_data(self):   # shot 폴더트리 선택시 실행되는 함수들
        if not self.ui.checkBox_avaliable_path.isChecked():
            self.change_current_path('shot_signal')
        self.change_shot_path()
        self.set_all_table_list('shot_signal')
        self.set_file_table_list('shot_signal')
        
    def event_tree_tab_changed(self,index):    # 폴더트리 탭 변경시 실행되는 함수들
        self.show_path(index)
        if index == 0:
            self.set_all_table_list('my_task_signal')
            self.set_file_table_list('my_task_signal')
            self.change_current_path('my_task_signal')
        elif index == 1:
            self.set_all_table_list('asset_signal')
            self.set_file_table_list('asset_signal')
            self.change_current_path('asset_signal')
        elif index == 2:
            self.set_all_table_list('shot_signal')
            self.set_file_table_list('shot_signal')
            self.change_current_path('shot_signal')
        
    def event_save_info_changed(self):  # 사용자가 버전이나 파일 타입 변경시 실행되는 함수들
        self.set_preview()
        self.set_work_area()
        
    def event_select_btn(self, button):   # select 버튼 작동
        shots_list = ["ani", "lgt", "mm", "cmp", "ly", "fx"]
        assets_list = ["mod","rig","lkd"]
        
        if button == "shots_all":
            for i in shots_list:
                getattr(self.ui,f"checkBox_{i}").setChecked(True)
        elif button == "shots_none":
            for i in shots_list:
                getattr(self.ui,f"checkBox_{i}").setChecked(False)
                
        if button == "assets_all":
            for i in assets_list:
                getattr(self.ui,f"checkBox_{i}").setChecked(True)
        elif button == "assets_none":
            for i in assets_list:
                getattr(self.ui,f"checkBox_{i}").setChecked(False)
        
    """
    외부 정보 불러오기_id로
    """
    def get_project_id(self):   # 프로젝트 데이터 가져오기 
        json_path = f'{self.root_path}/_phoenix_/Launcher/Loader/data_from_loader/json_from_loader.json'
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        # 254
        project_id = json_data['project_id']
        return project_id
    
    def get_user_id(self):   # 유저 정보 가져오기
        json_path = f'{self.root_path}/_phoenix_/Launcher/Loader/data_from_loader/json_from_loader.json'
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        # 90
        usr_id = json_data['user_id']
        return usr_id
    
    def get_project_name(self): # 프로젝트 이름받기 ★
        project_id = self.get_project_id()
        user_id = self.get_user_id()
        
        json_path = f'{self.project_json_path}/project{project_id}_user{user_id}.json'
        
        with open(json_path, 'r') as f:
            js_data = json.load(f)
        
        project_name = js_data['project']['name']
        return project_name
    
    def get_user_name(self):   # 유저 이름받기 ★
        project_id = self.get_project_id()
        user_id = self.get_user_id()
        
        json_path = f'{self.project_json_path}/project{project_id}_user{user_id}.json'
        
        with open(json_path, 'r') as f:
            js_data = json.load(f)
        
        user_name = js_data['user']['name']
        return user_name
    
    
    """ Asset """
    def get_assets_json_data(self):  # 에셋 json 데이터 가져오기 ★
        project_id = self.get_project_id()
        
        json_path = f'{self.project_json_path}/assets_proj{project_id}.json'
        with open(json_path, 'r') as f:
            js_data = json.load(f)
        
        return js_data
    
    def get_asset_types(self):  # 에셋 타입 데이터 가져오기 ★
        asset_data = self.get_assets_json_data()
        
        asset_type_list = []
        asset_list = asset_data['data']
        for asset in asset_list:
            if not asset['sg_asset_type'] in asset_type_list:
                asset_type_list.append(asset['sg_asset_type'])
            
        return asset_type_list
    
    def get_assets(self):   # 에셋 데이터 가져오기 ★
        asset_data = self.get_assets_json_data()
        assets = asset_data['data']
        
        return assets
    
    def get_asset_tasks(self, asset_id):    # 에셋 테스크 데이터 가져오기 ★
        project_id = self.get_project_id()
        
        json_path = f'{self.project_json_path}/asset_tasks_proj{project_id}.json'
        with open(json_path, 'r') as f:
            js_data = json.load(f)
        
        asset_task_list = js_data['data']
        asset_tasks =[]
        for asset_task in asset_task_list:
            if asset_task['asset_id'] == asset_id:
                asset_tasks.append(asset_task)
        
        return asset_tasks
    
    """ Shot """
    def get_sequences(self):    # 시퀀스 데이터 가져오기 ★
        project_id = self.get_project_id()
        
        json_path = f'{self.project_json_path}/sequences_proj{project_id}.json'
        with open(json_path, 'r') as f:
            js_data = json.load(f)
            
        sequences = js_data['data']
        
        return sequences
    
    def get_shots(self, sequence_id):   # 샷 데이터 가져오기 ★
        project_id = self.get_project_id()
        
        json_path = f'{self.project_json_path}/shots_proj{project_id}.json'
        with open(json_path, 'r') as f:
            js_data = json.load(f)
            
        shot_list = js_data['data']
        shots =[]
        
        for shot_data in shot_list:
            if not shot_data['sg_sequence']:
                continue
            if shot_data['sg_sequence']['id'] == sequence_id:
                shots.append(shot_data)
        
        return shots
    
    def get_shot_tasks(self, shot_id):   # 샷 테스크 데이터 가져오기 ★
        project_id = self.get_project_id()
        
        json_path = f'{self.project_json_path}/shot_tasks_proj{project_id}.json'
        with open(json_path, 'r') as f:
            js_data = json.load(f)
            
        shot_task_list = js_data['data']
        shot_tasks =[]
        for shot_task_data in shot_task_list:
            if not shot_task_data['shot_id'] == shot_id:
                pass
            shot_tasks.append(shot_task_data)
        
        return shot_tasks
    
    """ All """
    def get_assigned_work(self, user_id, project_id):   # 유저에게 배정된 작업만 가져오기(wtg,wip,pub) ★
        project_id = self.get_project_id()
        user_id = self.get_user_id()
        
        json_path = f'{self.project_json_path}/user{user_id}_assigned_tasks_proj{project_id}.json'
        with open(json_path, 'r') as f:
            js_data = json.load(f)
            
        shot_list = js_data['shot']
        asset_list = js_data['asset']
        
        return shot_list, asset_list
    
    def get_version(self, task_id): # wip, pub, version 데이터 가져오기 ★
        project_id = self.get_project_id()
    
        shot_ver_path = f'{self.project_json_path}/shot_versions_proj{project_id}.json'
        asset_ver_path = f'{self.project_json_path}/asset_versions_proj{project_id}.json'

        with open(shot_ver_path, 'r') as f:
            shot_task_list = json.load(f)['data']
        with open(asset_ver_path, 'r') as f:
            asset_task_list = json.load(f)['data']

        wip = pub = None
        versions = {'wip': None, 'pub': None}

        for shot_vers in shot_task_list:
            if shot_vers['task_id'] == task_id:
                wip_dic = shot_vers.get('wip', {})
                pub_dic = shot_vers.get('pub', {})

                wip = list(wip_dic.keys()) if wip_dic else None
                pub = list(pub_dic.keys()) if pub_dic else None

                versions = {'entity': 'Shots', 
                            'wip': wip_dic if wip_dic else None, 
                            'pub': pub_dic if pub_dic else None}
                break

        if not wip and not pub:  # 샷 리스트에 version이 없을 경우 에셋 리스트 확인
            for asset_vers in asset_task_list:
                if asset_vers['task_id'] == task_id:
                    wip_dic = asset_vers.get('wip', {})
                    pub_dic = asset_vers.get('pub', {})

                    wip = list(wip_dic.keys()) if wip_dic else None
                    pub = list(pub_dic.keys()) if pub_dic else None

                    versions = {'entity': 'Assets','wip': wip_dic if wip_dic else None, 'pub': pub_dic if pub_dic else None}
                    break
                
        return wip, pub, versions
        
    def get_thumbnail_list(self, task_id):   # 썸네일 가져오기 ★
        """
        주어진 task_id에 대해 썸네일 경로 리스트를 반환합니다.
        """
        proj_id = self.get_project_id()
        
        # JSON 파일 경로 설정
        shot_ver_path = f'{self.project_json_path}/shot_versions_proj{proj_id}.json'
        asset_ver_path = f'{self.project_json_path}/asset_versions_proj{proj_id}.json'

        # JSON 파일 로드
        with open(shot_ver_path, 'r') as f:
            shot_versions = json.load(f)['data']

        with open(asset_ver_path, 'r') as f:
            asset_versions = json.load(f)['data']

        # 버전 정보와 썸네일 경로를 저장할 딕셔너리
        thumbnail_list = []
        
        # 에셋 버전에서 썸네일 정보 찾기
        for asset_version in asset_versions:
            if asset_version['task_id'] == task_id:
                for status, versions in asset_version.items():
                    if status in ['wip', 'pub']:
                        for version_info in versions.values():
                            thumbnail_path = version_info.get('thumbnail', None)
                            version_id = version_info.get('id', None)
                            if version_id:
                                thumbnail_list.append({version_id: thumbnail_path})

        # 샷 버전에서 썸네일 정보 찾기
        for shot_version in shot_versions:
            if shot_version['task_id'] == task_id:
                for status, versions in shot_version.items():
                    if status in ['wip', 'pub']:
                        for version_info in versions.values():
                            thumbnail_path = version_info.get('thumbnail', None)
                            version_id = version_info.get('id', None)
                            if version_id:
                                thumbnail_list.append({version_id: thumbnail_path})

        return thumbnail_list
        
    def get_task_related_info(self, task_id):   # 선택한 테스크와 관련된 정보 가져오기.★
        """
        딕셔너리 형태로 출력
        ex)
        {
        'project_name': 'My Project',
        'project_id': 101,
        'task_name': 'Animation',
        'task_id': 1234,
        'shot_name': 'Shot_001',
        'shot_id': 202,
        'sequence_name': 'Seq_001',
        'sequence_id': 303
        }
        """
        project_id = self.get_project_id()
        project_name = self.get_project_name()

        # JSON 파일 경로 설정
        asset_task_path = os.path.join(self.project_json_path, f'asset_tasks_proj{project_id}.json')
        shot_task_path = os.path.join(self.project_json_path, f'shot_tasks_proj{project_id}.json')
        asset_version_path = os.path.join(self.project_json_path, f'asset_versions_proj{project_id}.json')
        shot_version_path = os.path.join(self.project_json_path, f'shot_versions_proj{project_id}.json')
        asset_file_path = os.path.join(self.project_json_path, f'assets_proj{project_id}.json')
        shot_file_path = os.path.join(self.project_json_path, f'shots_proj{project_id}.json')

        # JSON 파일 로드
        with open(asset_task_path, 'r', encoding='utf-8') as f:
            asset_tasks = json.load(f)['data']
        with open(shot_task_path, 'r', encoding='utf-8') as f:
            shot_tasks = json.load(f)['data']
        with open(asset_version_path, 'r', encoding='utf-8') as f:
            asset_versions = json.load(f)['data']
        with open(shot_version_path, 'r', encoding='utf-8') as f:
            shot_versions = json.load(f)['data']
        with open(asset_file_path, 'r', encoding='utf-8') as f:
            assets = json.load(f)['data']
        with open(shot_file_path, 'r', encoding='utf-8') as f:
            shots = json.load(f)['data']

        # 기본 task 정보
        task_info = {
            'project_name': project_name,
            'project_id': project_id,
            'task_id': task_id
        }
    
        # task_id에 맞는 에셋 정보 찾기
        for asset_task in asset_tasks:
            if not asset_task['id'] == task_id:
                continue
            for asset in assets:
                if not asset['id'] == asset_task['asset_id']:
                    continue
                for asset_version in asset_versions:
                    if not asset_version['task_id'] == task_id:
                        continue
                    task_info.update({
                        "task_name": asset_task.get('step_name', 'Unknown Task'),
                        "entity_type": "Asset",
                        "asset_id": asset['id'],
                        "asset_name": asset['code'],
                        "asset_type": asset['sg_asset_type'],
                        "latest_version": self.get_latest_version_code(asset_version.get('wip', {}), asset['code'],asset_task.get('step_name', 'Unknown Task'))
                    })
                    break
                break
            break
            
        # task_id에 맞는 샷 정보 찾기
        if "entity_type" not in task_info:  # 이미 에셋 정보가 채워졌는지 확인
            for shot_task in shot_tasks:
                if shot_task['id'] != task_id:
                    continue
                for shot in shots:
                    if shot['id'] != shot_task['shot_id']:
                        continue
                    for shot_version in shot_versions:
                        if shot_version['task_id'] != task_id:
                            continue
                        task_info.update({
                            "task_name": shot_task.get('step_name', 'Unknown Task'),
                            "entity_type": "Shot",
                            "shot_id": shot['id'],
                            "shot_name": shot['code'],
                            "sequence_name": shot['sg_sequence']['name'],
                            "sequence_id": shot['sg_sequence']['id'],
                            "latest_version": self.get_latest_version_code(shot_version.get('wip', {}),shot['code'], shot_task.get('step_name', 'Unknown Task'))
                        })
                        break
                    break
                break
            
        return task_info
   
    def get_latest_version_code(self, versions, asset_name, task_name): # wip파일중 가장 최신 버전의 파일 이름찾기
        """
        wip파일중 가장 최신 버전의 파일 이름을 찾습니다.
        버전이 없을 경우 해당되는 엔티티와 태스크에 맞춰 
        Ball_mod_v000과 같은 형태의 이름을 만들어줍니다.
        """
        
        max_version = None
        max_version_number = -1

        for ver_name in versions.keys():
            match = re.search(r'v(\d{3})$', ver_name)
            if match:
                version_number = int(match.group(1))
                if version_number > max_version_number:
                    max_version_number = version_number
                    max_version = ver_name

        return max_version if max_version else f'{asset_name}_{task_name}_v000'
   
    """
    외부 정보 불러오기_name으로
    """
    def get_sequence_id(self, project_id: int, sequence_name: str):    # 시퀀스 이름으로 시퀀스 ID 찾기
        """
        프로젝트 ID와 시퀀스 이름을 사용해 시퀀스의 ID를 가져옵니다.
        :param project_id: 프로젝트 ID
        :param sequence_name: 시퀀스 이름
        :return: 시퀀스 ID
        """
        sequence_file_path = os.path.join(self.project_json_path, f'sequences_proj{project_id}.json')

        with open(sequence_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)['data']

        # 시퀀스 이름에 해당하는 시퀀스 찾기
        for seq in data:
            if seq['code'] == sequence_name:
                sequence_id = seq['id']
                break
        # 시퀀스 ID 반환
        return sequence_id
        
    def get_shot_id(self, sequence_id: int, shot_name: str): # 샷 이름으로 샷 ID 찾기 
        """
        시퀀스 ID와 샷 이름을 사용해 샷의 ID를 가져옵니다.
        :param sequence_id: 시퀀스 ID
        :param shot_name: 샷 이름
        :return: 샷 ID (없으면 None 반환)
        """
        project_id = self.get_project_id()
        shot_file_path = os.path.join(self.project_json_path, f'shots_proj{project_id}.json')

        with open(shot_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)['data']

        # 시퀀스 ID와 샷 이름에 해당하는 샷 찾기
        for shot in data:
            if not shot['sg_sequence']:
                continue
            if shot['sg_sequence']['id'] == sequence_id and shot['code'] == shot_name:
                shot_id = shot['id']
                break

        return shot_id
    
    def get_asset_id(self, project_id: int, asset_name: str):   # 에셋 이름으로 에셋 ID 찾기
        """
        프로젝트 ID와 에셋 이름을 사용해 에셋의 ID를 가져옵니다.
        :param project_id: 프로젝트 ID
        :param asset_name: 에셋 이름
        :return: 에셋 ID (없으면 None 반환)
        """
        # 에셋 JSON 파일 경로
        asset_file_path = os.path.join(self.project_json_path, f'assets_proj{project_id}.json')

        # JSON 파일 로드
        with open(asset_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)['data']

        # 에셋 이름에 해당하는 에셋 찾기
        asset_id = None
        for asset in data:
            if asset['code'] == asset_name:
                asset_id = asset['id']
                break

        return asset_id
        
    def get_task_id(self, entity_id: int, entity_type: str ,task_name: str): # 테스크 이름으로 테스크 ID 찾기
        """
        샷 또는 에셋의 ID와 태스크 이름을 사용해 태스크의 ID를 가져옵니다.
        :param entity_id: 샷 또는 에셋의 ID
        :param entity_type: "Shot" 또는 "Asset"
        :param task_name: 태스크 이름
        :return: 태스크 ID (없으면 None 반환)
        """
        project_id = self.get_project_id()
        # 적절한 JSON 파일 경로를 설정
        if entity_type == "Shot":
            task_file_path = os.path.join(self.project_json_path, f'shot_tasks_proj{project_id}.json')
        elif entity_type == "Asset":
            task_file_path = os.path.join(self.project_json_path, f'asset_tasks_proj{project_id}.json')

        with open(task_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)['data']
            
        # 태스크 ID를 찾기
        for task in data:
            if entity_type == "Shot":
                if task['shot_id'] == entity_id and task['step_name'] == task_name:
                    task_id = task['id']
            elif entity_type == "Asset":
                if task['asset_id'] == entity_id and task['step_name'] == task_name:
                    task_id = task['id']
                
        return task_id
        
    """
    기타 함수
    """
    def check_file_version(self): # 기존 파일들 버전 체크, str 출력
        """
        v001과 같은 형식으로 형태만 버전의 남겨주는 함수입니다.
        """
        file_name_with_ver = os.path.basename(current_path)
        
        p = re.compile('v\d{3}')
        p_data = p.search(file_name_with_ver)
        
        if p_data:
            version = p_data.group()
        return version
    
    def check_file_type(self):  # 현재 열린 파일이 어떤 종류인지 체크 
        print(f"현재 경로 : {current_path}")
        ext = None
        if not current_path:
            print("경로가 안잡힘")
            return
        file_name = current_path.split("/")[-1]
        ext = file_name.split(".")[-1]
    
        return ext
    
    def check_right_entity(self):   # 파일 저장 전 entity가 같은 곳인지 체크
        entity_check = False
        _, current_entity = self.get_shotgrid_directory()
        
        root_folder = "/phoenix_pipeline_folders/"
        p = re.compile(rf"{root_folder}(.+?)/(Shots|Assets)/(.+?)/[^/]+$")
        p_data = p.search(self.initial_path) 
        if p_data:
            original_entity = p_data.group(2)
            
        if current_entity == original_entity:
           entity_check = True
        return entity_check 
    
    def check_shotgrid_version(self):   # 현재 지정된 경로에 따라 샷그리드에서 버전 체크
        save_info,_ = self.store_save_info()
        task_id = save_info['task']['id']
        wips,_,_ = self.get_version(task_id)
        
        now_ver = '000'
        next_ver = '001'
        
        if not wips:
            return now_ver, next_ver
            
        ver_list = []
        for wip in wips:
            p = re.compile("v(\d{3})")
            p_data = p.search(wip)
            if p_data:
                wip_ver = p_data.group(1)
                ver_list.append(wip_ver)
        if ver_list:
            now_ver = sorted(ver_list)[-1]
            next_ver_num = int(now_ver) + 1
            next_ver = str(next_ver_num).zfill(3)
        
        return now_ver, next_ver
        
    def get_shotgrid_directory(self):   # 현재 경로에서 샷그리드 관련 경로 찾기
        # 경로 안바꿀때 
        # 경로 바꿀때 두가지로 작동
        root_folder = "/phoenix_pipeline_folders/"
        p = re.compile(rf"{root_folder}(.+?)/(Shots|Assets)/(.+?)/[^/]+$")
        p_data = p.search(current_path) 
        if p_data:
            extracted_path = os.path.join(p_data.group(1), p_data.group(3))
            entity_type = p_data.group(2)
        return extracted_path, entity_type
    
    def store_save_info(self):  # 저장될 경로에 필요한 정보 저장
        """
        {'project' : {'name' : project_name, 'id' : project_id}, 
        'sequence' : {'name': seq_name, 'id' : seq_id}, 
        'shot' : {'name': shot_name, 'id' : shot_id}, 
        'task' : {'name': task_name,'id':task_id}}
        
        {'project' : {'name' : project_name, 'id' : project_id}, 
        'asset_type' : {'name': asset_type_name}, 
        'asset' : {'name': asset_name, 'id' : asset_id}, 
        'task' : {'name': task_name,'id':task_id}}
        """
        total_dic = {}
        extracted_path,entity_type = self.get_shotgrid_directory()
        project_name = extracted_path.split('/')[0]
        project_id = self.get_project_id()
        
        # 샷 정보
        if entity_type == "Shots":
            seq_name = extracted_path.split('/')[1]
            seq_id = self.get_sequence_id(project_id, seq_name)
            shot_name = extracted_path.split('/')[2]
            shot_id = self.get_shot_id(seq_id, shot_name)
            task_name = extracted_path.split('/')[3]
            task_id = self.get_task_id(shot_id,"Shot",task_name)
            
            total_dic['project'] = {'name' : project_name, 'id' : project_id}
            total_dic['sequence'] = {'name' : seq_name, 'id' : seq_id}
            total_dic['shot'] = {'name' : shot_name, 'id' : shot_id}
            total_dic['task'] = {'name' : task_name, 'id' : task_id}
            
        # 에셋 정보
        if entity_type == "Assets":
            asset_type_name = extracted_path.split('/')[1]
            asset_name = extracted_path.split('/')[2]
            asset_id = self.get_asset_id(project_id, asset_name)
            task_name = extracted_path.split('/')[3]
            task_id = self.get_task_id(asset_id,"Asset",task_name)
            
            total_dic['project'] = {'name' : project_name, 'id' : project_id}
            total_dic['asset_type'] = {'name' : asset_type_name}
            total_dic['asset'] = {'name' : asset_name, 'id' : asset_id}
            total_dic['task'] = {'name' : task_name, 'id' : task_id}
            
        return total_dic, entity_type
    
    def store_changed_path(self):   # 바뀐 경로 저장해두기
        changed_path = current_path
        print(f"---------바뀐 경로 : {changed_path}------------------")
        return changed_path
    
    def select_path(self): # 기존 경로로 할지 바뀐 경로로 할지 정해줌
        global current_path
        index = self.ui.tabWidget_pathtree.currentIndex()
        if not self.ui.checkBox_avaliable_path.isChecked():
            if index == 0:
                self.change_current_path('my_task_signal')
            elif index == 1:
                self.change_current_path('asset_signal')
            elif index == 2:
                self.change_current_path('shot_signal')
        else:
            current_path = self.initial_path
        self.setup_bottom_layer()    
    
    def find_task_id_item(self, tree_widget, task_id, current_item = None):    # 트리위젯에서 task_id를 가진 아이템을 리턴 
        """
        QTreeWidget에서 주어진 task_id를 가진 아이템을 찾습니다.
        
        return: task_id를 가진 QTreeWidgetItem (없으면 None 반환)
        """
        if current_item == None:
            for i in range(tree_widget.topLevelItemCount()):
                current_item  = tree_widget.topLevelItem(i)
                found_item = self.find_task_id_item(tree_widget, task_id, current_item)  # 재귀 호출
                if found_item:
                    return found_item
            
        if not current_item.data(0,Qt.UserRole):
            pass
        if current_item.data(0, Qt.UserRole) == task_id:
            return current_item
        
        if current_item.childCount() != 0:
            for j in range(current_item.childCount()):
                found_item = self.find_task_id_item(tree_widget, task_id, current_item.child(j))
                if found_item:
                    return found_item
                
        # 아이템을 찾지 못한 경우
        return None

    """
    Json 파일이 만들어지기까지 로딩페이지 보여주는 함수
    """
    def show_loading_page(self):    # 로딩 페이지 보여주기
        project_id = self.get_project_id()
        user_id = self.get_user_id()
        
        # GIF 이미지 시작
        movie = QMovie(f"{self.root_path}/_phoenix_/ui/image_source/Dark-Phoenix4.gif")
        self.ui.label_gif.setMovie(movie)
        movie.start()
        
        # QPlainTextEdit을 stdout에 연결합니다.
        self.redirect_stdout_to_label()
        
        # ShotgridWorker 스레드를 설정하고 시작합니다.
        shotgridworker = ShotgridWorker(project_id, user_id)
        shotgridworker.on_task_finished = self.on_task_finished # 작업 완료 시 호출될 메서드 설정
        shotgridworker.start()

        # 로딩 화면 보여주기
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_task_finished(self): # Json파일이 다 만들어지면 Saver UI 메인 화면 보여주기
        # 스레드 작업이 완료되면 호출됩니다.
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.label_gif.movie().stop()
        
        # stdout 원래대로 복원하기
        sys.stdout = self.original_stdout
        
        # self.first_show()
        

    def redirect_stdout_to_label(self): # stdout을 지정한 라벨로 옮겨주기
        """라벨에 stdout을 리다이렉트합니다."""
        sys.stdout = self
        
    def write(self, message):  # 라벨에 stdout을 띄워주기
        """라벨에 메시지를 추가하는 메서드입니다."""
        current_text = self.ui.label_print_status.text()
        new_text = f"{current_text}\n{message}"
        
        # 줄 단위로 텍스트를 분리
        lines = new_text.splitlines()
        
        # 줄 수가 최대 줄 수를 초과하면 첫 번째 줄을 제거
        if len(lines) > 6:
            lines = lines[-6:]
            
        # 줄을 다시 하나의 문자열로 합치기
        updated_text = "\n".join(lines)
        
        self.ui.label_print_status.setText(updated_text)
        
    def flush(self):
        """파일과 같은 인터페이스를 위해 flush 메서드를 추가합니다."""
        pass

    def closeEvent(self, event):    # 윈도우가 꺼지면 스레드를 안전하게 종료시킴
        """
        윈도우를 닫을 때 스레드가 아직 실행 중인 경우 안전하게 종료하도록 합니다.
        """
        if hasattr(self, 'shotgridworker'): # 객체(self)에 특정 속성(shotgridworker, 문자열)이 존재하는지를 확인하는 코드
            self.shotgridworker.stop()
        event.accept()
    
    """
    Search 기능 관련 함수
    """
    def setup_search_mode(self):    # 검색 기능 셋팅
        self.search_timer = QTimer(self)    # 검색 타이머 생성
        self.search_timer.setSingleShot(True)   # 한 번만 실행되도록 설정
        self.search_timer.timeout.connect(self.perform_search)  # 타임아웃 시 perform_search 메서드 호출
        self.current_search_widget = None  # 현재 검색 중인 위젯을 추적하는 변수 추가
        
    def start_search_timer(self):   # 입력 전 너무 빨리 검색하는 것 방지하기 위한 시간
        self.current_search_widget = self.sender()  # 현재 검색 중인 위젯 설정
        self.search_timer.start(300)   # 300ms 후에 검색 실행
        
    def perform_search(self):   # 검색창에 따라 검색할 트리 할당
        if self.current_search_widget:
            search_text = self.current_search_widget.text().lower()
            
            if self.current_search_widget == self.ui.lineEdit_search_my_tasks:
                self.filter_tree(self.ui.treeWidget_my_tasks, search_text)
            elif self.current_search_widget == self.ui.lineEdit_search_assets:
                self.filter_tree(self.ui.treeWidget_assets, search_text)
            elif self.current_search_widget == self.ui.lineEdit_search_shots:
                self.filter_tree(self.ui.treeWidget_shots, search_text)
            # 버전 검색 기능
            elif self.current_search_widget == self.ui.lineEdit_search_all:
                self.filter_all_versions(search_text)
            elif self.current_search_widget == self.ui.lineEdit_search_wip:
                self.filter_versions(self.ui.tableWidget_list_wip, search_text)
            elif self.current_search_widget == self.ui.lineEdit_search_pub:
                self.filter_versions(self.ui.tableWidget_list_pub, search_text)
        else:
            print("현재 검색 중인 위젯이 없습니다.")
            
    def filter_tree(self, tree: QTreeWidget, search_text: str): # 할당된 트리의 첫 아이템 찾기
        """
        검색이 시작된 트리의 첫 아이템부터 재귀적 검사를 시행합니다.
        """
        # 루트 아이템부터 시작하여 모든 아이템을 재귀적으로 검사
        root = tree.invisibleRootItem()
        self.filter_tree_item(root, search_text)
        
    def filter_tree_item(self, item: QTreeWidgetItem, search_text: str) -> bool:    # 트리 아이템 필터링
        """
        검색어와 맞지 않는 아이템들을 hidden시켜줍니다.
        검색어에 할당되는 아이템들을 parent아이템까지 모두 보여줍니다.
        """
        # 현재 아이템의 텍스트가 검색어를 포함하는지 확인
        item_visible = False
        if search_text in item.text(0).lower():
            item_visible = True
        
        
        # 자식 아이템들을 검사
        child_count = item.childCount() 
        for i in range(child_count):  
            child = item.child(i)  
            if self.filter_tree_item(child, search_text):   # 자식 아이템 필터링
                item_visible = True
        
        # 아이템의 가시성 설정
        if item_visible:
            item.setHidden(False)
        else:
            item.setHidden(True)
        
        return item_visible

    def filter_all_versions(self, search_text: str):    # all 트리 아이템 필터링
        """
        테이블 위젯에서 버전 네임을 검색하여 일치하지 않는 행을 숨깁니다.
        """
        root = self.ui.treeWidget_grid_total.invisibleRootItem()  # 트리의 루트 아이템 가져오기
        child_count = root.childCount()  # 자식 아이템 수
        for i in range(child_count):
            parent_item = root.child(i)  # 부모 아이템 (Working 또는 Publishes)
            table_widget = self.ui.treeWidget_grid_total.itemWidget(parent_item.child(0), 0)  # 테이블 위젯 가져오기
            if isinstance(table_widget, QTableWidget):
                for row in range(table_widget.rowCount()):
                    cell_widget = table_widget.cellWidget(row, 1)  # 버전 이름이 있는 셀 가져오기
                    if isinstance(cell_widget, QPlainTextEdit):
                        version_name = cell_widget.toPlainText().splitlines()[1]  # 두 번째 라인에 버전 네임이 있다고 가정
                        if search_text.lower() in version_name.lower():
                            table_widget.setRowHidden(row, False)  # 검색어와 일치하면 행을 표시
                        else:
                            table_widget.setRowHidden(row, True)  # 검색어와 일치하지 않으면 행을 숨김
    
    def filter_versions(self, table_widget: QTableWidget, search_text: str):    # wip, pub 테이블 위젯 필터링
        """
        테이블 위젯에서 버전 네임을 검색하여 일치하지 않는 행을 숨깁니다.
        """
        for row in range(table_widget.rowCount()):
            cell_widget = table_widget.cellWidget(row, 1)  # 버전 이름이 있는 셀 가져오기
            if isinstance(cell_widget, QPlainTextEdit):
                version_name = cell_widget.toPlainText().splitlines()[1]  # 두 번째 라인에 버전 네임이 있다고 가정
                if search_text.lower() in version_name.lower():
                    table_widget.setRowHidden(row, False)  # 검색어와 일치하면 행을 표시
                else:
                    table_widget.setRowHidden(row, True)  # 검색어와 일치하지 않으면 행을 숨김
    
    """
    Filter 기능 관련 함수
    """
    def filter_tree_by_checkboxes(self):
        """
        체크박스 상태에 따라 treeWidget_assets 또는 treeWidget_shots를 필터링합니다.
        'mod', 'rig', 'lkd' 체크박스는 treeWidget_assets를 필터링하고,
        'ani', 'lgt', 'cmp', 'mm' 체크박스는 treeWidget_shots를 필터링합니다.
        """
        # Asset 체크박스 상태를 리스트로 저장
        asset_checked_types = []
        if self.ui.checkBox_mod.isChecked():
            asset_checked_types.append('mod')
        if self.ui.checkBox_rig.isChecked():
            asset_checked_types.append('rig')
        if self.ui.checkBox_lkd.isChecked():
            asset_checked_types.append('lkd')

        # Shot 체크박스 상태를 리스트로 저장
        shot_checked_types = []
        if self.ui.checkBox_ani.isChecked():
            shot_checked_types.append('ani')
        if self.ui.checkBox_lgt.isChecked():
            shot_checked_types.append('lgt')
        if self.ui.checkBox_cmp.isChecked():
            shot_checked_types.append('cmp')
        if self.ui.checkBox_mm.isChecked():
            shot_checked_types.append('mm')
        if self.ui.checkBox_ly.isChecked():
            shot_checked_types.append('ly')
        if self.ui.checkBox_fx.isChecked():
            shot_checked_types.append('fx')

        # treeWidget_assets 필터링
        root_assets = self.ui.treeWidget_assets.invisibleRootItem()
        self.filter_item(root_assets, asset_checked_types)

        # treeWidget_shots 필터링
        root_shots = self.ui.treeWidget_shots.invisibleRootItem()
        self.filter_item(root_shots, shot_checked_types)
        
    def filter_item(self, item: QTreeWidgetItem, checked_types: list) -> bool:
        """
        주어진 아이템과 자식 아이템을 필터링하고, 조건에 맞는 아이템을 표시합니다.
        """
        item_visible = False
        child_count = item.childCount()

        # 자식 아이템을 재귀적으로 필터링
        for i in range(child_count):
            child = item.child(i)
            if self.filter_item(child, checked_types):
                item_visible = True

        # 현재 아이템이 조건에 맞는지 검사
        item_text = item.text(0).lower()
        for checked_type in checked_types:
            if checked_type in item_text:
                item_visible = True
                break  # 하나라도 포함되면 더 이상 검사할 필요 없음

        # 아이템의 가시성 설정
        item.setHidden(not item_visible)

        return item_visible


    """
    기본 표시 셋팅
    """
    def first_show(self): # 기본 셋팅
        # 유저 이름 넣기
        user_name = self.get_user_name()
        self.ui.label_user_name.setText(user_name)
        # project 이름 넣기
        proj_name = self.get_project_name()
        self.ui.label_project_name.setText(proj_name)
        # 기본 ui 셋팅
        self.ui.stackedWidget_path.setCurrentIndex(0)
        self.ui.tabWidget_pathtree.setCurrentIndex(0)
        self.ui.tabWidget_file_list.setCurrentIndex(0)
        self.ui.comboBox_filter.setCurrentIndex(0)
        self.ui.checkBox_avaliable_ver.setChecked(True)
        self.ui.checkBox_avaliable_path.setChecked(True)
        # 필터 체크박스 셋팅
        self.ui.checkBox_mod.setChecked(True)
        self.ui.checkBox_rig.setChecked(True)
        self.ui.checkBox_lkd.setChecked(True)
        self.ui.checkBox_ani.setChecked(True)
        self.ui.checkBox_lgt.setChecked(True)
        self.ui.checkBox_cmp.setChecked(True)
        self.ui.checkBox_mm.setChecked(True)
        self.ui.checkBox_ly.setChecked(True)
        self.ui.checkBox_fx.setChecked(True)
        # 좌측 레이어 셋팅
        self.set_path_filter()
        self.set_my_tasks_tree()
        self.set_asset_path_tree()
        self.set_shot_path_tree()
        self.show_current_path_tree()
        # 하단 레이어 셋팅
        self.setup_bottom_layer()
        # 이미지 추가
        self.add_image()
    
    def add_image(self):    # UI에 이미지 추가
        # 로딩화면에 peonix 아이콘 추가
        peonix_path = f"{self.root_path}/_phoenix_/ui/image_source/desktop_icon.png"
        pixmap = QPixmap(peonix_path)
        sc_pixmap = pixmap.scaledToWidth(100)
        self.ui.label_main_icon.setPixmap(sc_pixmap)
        
        # Saver home에 peonix 아이콘 추가
        peonix_path = f"{self.root_path}/_phoenix_/ui/image_source/desktop_icon.png"
        h_pixmap = QPixmap(peonix_path)
        h_sc_pixmap = h_pixmap.scaledToWidth(40)
        self.ui.label_icon.setPixmap(h_sc_pixmap)
        
        # user 아이콘 추가
        user_icon_path = f"{self.root_path}/_phoenix_/ui/image_source/icon_profile.png"
        u_pixmap = QPixmap(user_icon_path)
        u_sc_pixmap = u_pixmap.scaledToWidth(30)
        self.ui.label_user_icon.setPixmap(u_sc_pixmap)
    
    """
    좌 레이어 셋팅
    """
    def show_current_path_tree(self):   # 현재 파일 경로에 맞게 파일트리 아이템을 선택하기.
        """
        처음 UI가 켜질 때, My Tasks 트리 위젯에서 현재 경로에 맞는 파일 트리 아이템을 선택해둡니다.
        Shot 파트일 경우 Shots 트리위젯 아이템 또한 선택됩니다.
        Asset 파트일 경우 Assets 트리위젯 아이템 또한 선택됩니다.
        """
        save_info, entity_type = self.store_save_info()
        task_id = save_info['task']['id']
        my_tasks_item = self.find_task_id_item(self.ui.treeWidget_my_tasks, task_id)
        if my_tasks_item:
            self.ui.treeWidget_my_tasks.setCurrentItem(my_tasks_item)
            pass
        
        if entity_type == 'Shots':
            item = self.find_task_id_item(self.ui.treeWidget_shots, task_id)
            self.ui.treeWidget_shots.setCurrentItem(item)
            
        elif entity_type == 'Assets':
            item = self.find_task_id_item(self.ui.treeWidget_assets, task_id)
            self.ui.treeWidget_assets.setCurrentItem(item)
        
    def show_path(self,index):    # 상단 경로 Tasks, Assets, Shots 별로 바꿔주기
        self.ui.stackedWidget_path.setCurrentIndex(index)
        
    def set_path_filter(self):  # My Tasks 폴더구조 트리 필터
        filter_list = ["All","Duration(Work)"]
        self.ui.comboBox_filter.addItems(filter_list)
        
    """ My Tasks """
    def change_my_tasks_path(self):     #My Tasks 상단 경로 바꿔주기
        selected_item = self.ui.treeWidget_my_tasks.currentItem()
        if selected_item.parent() == None:
            pass
        elif selected_item.parent().parent() == None:
            part = selected_item.text(0)
            self.ui.label_part.setText(part)
            
            self.ui.label_arrow_1.clear()
            self.ui.label_detail.clear()
        else:
            part = selected_item.parent().text(0)
            detail = selected_item.text(0)
            self.ui.label_part.setText(part)
            self.ui.label_arrow_1.setText('▶')
            self.ui.label_detail.setText(detail)
    
    def set_my_tasks_tree(self):    # My Tasks 폴더구조 트리 띄우기
        self.ui.treeWidget_my_tasks.clear()
        user_id = self.get_user_id()
        project_id = self.get_project_id()
        shot_list, asset_list = self.get_assigned_work(user_id,project_id)
        
        if shot_list:
            # 'Shots' 항목 추가
            shot_title_item = QTreeWidgetItem(self.ui.treeWidget_my_tasks)
            shot_title_item.setText(0, 'Shots')
            shot_title_item.setExpanded(True)
            
            # Sequence와 Shot을 트리에 추가
            for asset_dict in shot_list:
                seq_name = asset_dict['sequence']['name']
                seq_id = asset_dict['sequence']['id']
                shot_name = asset_dict['shot']['name']
                task_id = asset_dict['task']['id']
                
                
                # Sequence 항목을 찾거나 생성
                seq_item = None
                for i in range(shot_title_item.childCount()):
                    if shot_title_item.child(i).text(0) == seq_name:
                        seq_item = shot_title_item.child(i)
                        break

                if not seq_item:
                    seq_item = QTreeWidgetItem(shot_title_item)
                    seq_item.setText(0, seq_name)
                    seq_item.setData(0, Qt.UserRole, seq_id)
                
                # Shot 항목 추가
                shot_item = QTreeWidgetItem(seq_item)
                shot_item.setText(0, shot_name)
                shot_item.setData(0, Qt.UserRole, task_id)
        if asset_list:
            # 'Assets' 항목 추가
            asset_title_item = QTreeWidgetItem(self.ui.treeWidget_my_tasks)
            asset_title_item.setText(0, 'Assets')
            asset_title_item.setExpanded(True)
            
            # Asset Type과 Asset을 트리에 추가
            for asset_dict in asset_list:
                asset_type_name = asset_dict['asset_type']
                asset_name = asset_dict['asset']['name']
                task_id = asset_dict['task']['id']
                
                # Asset Type 항목을 찾거나 생성
                asset_type_item = None
                for i in range(asset_title_item.childCount()):
                    if asset_title_item.child(i).text(0) == asset_type_name:
                        asset_type_item = asset_title_item.child(i)
                        break

                if not asset_type_item:
                    asset_type_item = QTreeWidgetItem(asset_title_item)
                    asset_type_item.setText(0, asset_type_name)
                
                # Asset 항목 추가
                asset_item = QTreeWidgetItem(asset_type_item)
                asset_item.setText(0, asset_name)
                asset_item.setData(0,Qt.UserRole, task_id)
                
    """ Asset """
    def change_asset_path(self): # Asset 상단 경로 바꿔주기 
        selected_item = self.ui.treeWidget_assets.currentItem()
        if selected_item.parent() == None:
            asset_type = selected_item.text(0)
            self.ui.label_asset_type.setText(asset_type)
            
            self.ui.label_arrow_2.clear()
            self.ui.label_asset.clear()
            self.ui.label_arrow_3.clear()
            self.ui.label_asset_task.clear()
        elif selected_item.parent().parent() == None:
            asset_type = selected_item.parent().text(0)
            shot = selected_item.text(0)
            self.ui.label_asset_type.setText(asset_type)
            self.ui.label_arrow_2.setText("▶")
            self.ui.label_asset.setText(shot)
            
            self.ui.label_arrow_3.clear()
            self.ui.label_asset_task.clear()
        else:
            asset_type = selected_item.parent().parent().text(0)
            shot = selected_item.parent().text(0)
            task = selected_item.text(0)
            self.ui.label_asset_type.setText(asset_type)
            self.ui.label_arrow_2.setText("▶")
            self.ui.label_asset.setText(shot)
            self.ui.label_arrow_3.setText("▶")
            self.ui.label_asset_task.setText(task)
        
    def set_asset_path_tree(self):  # Asset 폴더구조 트리 띄우기 ★
        self.ui.treeWidget_assets.clear()
        asset_type_list = self.get_asset_types()
        assets = self.get_assets()
        
        for asset_type in asset_type_list:
            asset_type_item = QTreeWidgetItem(self.ui.treeWidget_assets)
            asset_type_item.setText(0, asset_type)
            for asset in assets:
                if not asset['sg_asset_type'] == asset_type:
                    continue
                asset_item = QTreeWidgetItem(asset_type_item)
                asset_item.setText(0,asset['code'])
                asset_item.setData(0, Qt.UserRole, asset['id'])   # item에 데이터 담기
                tasks = self.get_asset_tasks(asset['id'])
                for task in tasks:
                    if task['step_name'] == 'Unknown Step':
                        continue
                    if not task['asset_id'] == asset['id']:
                        continue 
                    task_item = QTreeWidgetItem(asset_item)
                    task_item.setText(0, task['step_name'])
                    task_item.setData(0, Qt.UserRole, task['id'])
            
    """ Shot """
    def change_shot_path(self): # Shot 상단 경로 바꿔주기
        selected_item = self.ui.treeWidget_shots.currentItem()
        if selected_item.parent() == None:
            seq = selected_item.text(0)
            self.ui.label_seq.setText(seq)
            
            self.ui.label_arrow_4.clear()
            self.ui.label_shot.clear()
            self.ui.label_arrow_5.clear()
            self.ui.label_shot_task.clear()
        elif selected_item.parent().parent() == None:
            seq = selected_item.parent().text(0)
            shot = selected_item.text(0)
            self.ui.label_seq.setText(seq)
            self.ui.label_arrow_4.setText("▶")
            self.ui.label_shot.setText(shot)
            
            self.ui.label_arrow_5.clear()
            self.ui.label_shot_task.clear()
        else:
            seq = selected_item.parent().parent().text(0)
            shot = selected_item.parent().text(0)
            task = selected_item.text(0)
            self.ui.label_seq.setText(seq)
            self.ui.label_arrow_4.setText("▶")
            self.ui.label_shot.setText(shot)
            self.ui.label_arrow_5.setText("▶")
            self.ui.label_shot_task.setText(task)
        
    def set_shot_path_tree(self):    # Shot 폴더구조 트리 띄우기 ★
        self.ui.treeWidget_shots.clear()
        sequences = self.get_sequences()
        
        for seq in sequences:
            seq_item = QTreeWidgetItem(self.ui.treeWidget_shots)
            seq_item.setText(0, seq['code'])
            seq_item.setData(0, Qt.UserRole, seq['id'])
            shots = self.get_shots(seq['id'])
            for shot in shots:
                shot_item = QTreeWidgetItem(seq_item)
                shot_item.setText(0,shot['code'])
                shot_item.setData(0, Qt.UserRole, shot['id'])   # item에 데이터 담기
                tasks = self.get_shot_tasks(shot['id'])
                for task in tasks:
                    if task['step_name'] == 'Unknown Step':
                        continue
                    if not task['shot_id'] == shot['id']:
                        continue 
                    task_item = QTreeWidgetItem(shot_item)
                    task_item.setText(0, task['step_name'])
                    task_item.setData(0, Qt.UserRole, task['id'])
       
        
    """
    우 레이어 셋팅
    """
    def set_thumbnail(self, table_widget, row, ver_id, thumbnail_list): # 썸네일을 테이블 위젯의 특정 셀에 설정
        """
        썸네일을 테이블 위젯의 특정 셀에 설정합니다.
        """
        thumbnail_path = next((thumbnail_dic.get(ver_id, "") for thumbnail_dic in thumbnail_list if ver_id in thumbnail_dic), "")
        thumbnail = QLabel()
        if thumbnail_path == 'No Thumbnail':
            thumbnail.setText("No Image")
            thumbnail.setAlignment(Qt.AlignCenter)
        else:
            pix = QPixmap(thumbnail_path)
            sc_pix = pix.scaledToWidth(100)
            thumbnail.setPixmap(sc_pix)
        table_widget.setCellWidget(row, 0, thumbnail)

    def adjust_table_size(self, table_widget):  # 테이블 위젯 높이 조절
        """
        테이블 위젯의 높이를 데이터에 맞게 자동 조정합니다.
        """
        default_row_height = 71.4
        total_height = table_widget.rowCount() * default_row_height

        # 테이블의 높이를 조정합니다.
        table_widget.setFixedHeight(total_height)
        
    def fill_table_with_data(self, table_widget, status_list, versions, thumbnail_list, status_type):    # 데이터를 테이블 위젯에 채우기
        """
        WIP 또는 Pub 데이터를 테이블 위젯에 채우는 함수입니다.
        """
        if not status_list:
            return
        
        # 테이블 위젯의 행 수를 데이터 목록의 길이로 설정
        table_widget.setRowCount(len(status_list))
        
        # 탭 위젯 이름 옆에 가진 파일 갯수 표시
        if status_type == 'wip':
            self.ui.tabWidget_file_list.setTabText(1, f'Working({len(status_list)})')
        if status_type == 'pub':
            self.ui.tabWidget_file_list.setTabText(2, f'Publishes({len(status_list)})')
        
        row = 0
        for status in status_list:
            version_info = versions.get(status_type, {}).get(status, {})
            ver_id = version_info.get('id', None)
            file_type = version_info.get('file_type') or 'Unknown'
            artist = version_info.get('artist') or 'Unknown'
            date = version_info.get('created_at') or 'Unknown'

            # 썸네일 설정
            self.set_thumbnail(table_widget, row, ver_id, thumbnail_list)

            # 텍스트 정보 설정
            info_text = QPlainTextEdit()
            font = QFont()
            font.setPointSize(8)
            info_text.setFont(font)
            info_text.appendPlainText(file_type)
            info_text.appendPlainText(status)
            info_text.appendPlainText(artist)
            info_text.appendPlainText(date)
            info_text.setFixedHeight(70)
            info_text.setReadOnly(True)
            info_text.setStyleSheet("QPlainTextEdit { border: none; }")
            table_widget.setCellWidget(row, 1, info_text)
            
            # 행 높이 조정
            table_widget.setRowHeight(row, 70)
            
            row += 1
            
        # 테이블 사이즈 조정    
        if table_widget in self.ui.treeWidget_grid_total.findChildren(QTableWidget):
            self.adjust_table_size(table_widget)    
            
    def initialize_table_widget(self, table_widget):    # 테이블 위젯 기본 설정
        """
        테이블 위젯의 기본 설정을 초기화합니다.
        """
        table_widget.setColumnCount(2)
        table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table_widget.horizontalHeader().setVisible(False)
        table_widget.horizontalHeader().setStretchLastSection(True)
        table_widget.verticalHeader().setVisible(False)
        table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        # 행 수에 따라 높이 초기화
        table_widget.setRowCount(0)

    def set_all_table_list(self, filter):   #  WIP 및 Pub 파일을 동시에 보여주기 ★
        """
        WIP 및 Pub 파일을 동시에 보여주는 함수입니다.
        """
        # 기존 테이블 위젯의 내용을 초기화
        self.ui.treeWidget_grid_total.clear()

        # 필터에 따라 선택된 항목을 가져오기
        if filter == 'my_task_signal':
            selected_item = self.ui.treeWidget_my_tasks.currentItem()
        elif filter == 'asset_signal':
            selected_item = self.ui.treeWidget_assets.currentItem()
        elif filter == 'shot_signal':
            selected_item = self.ui.treeWidget_shots.currentItem()

        # 선택된 항목 확인
        if selected_item is None or selected_item.childCount() != 0:
            return

        # 선택된 항목에서 정보값들 가져오기
        task_id = selected_item.data(0, Qt.UserRole)
        wips, pubs, versions = self.get_version(task_id)
        thumbnail_list = self.get_thumbnail_list(task_id) or []

        # 'Working' 및 'Publishes' 항목 추가
        working_item = QTreeWidgetItem(self.ui.treeWidget_grid_total)
        working_item.setText(0, 'Working')
        working_item.setExpanded(True)
        publishes_item = QTreeWidgetItem(self.ui.treeWidget_grid_total)
        publishes_item.setText(0, 'Publishes')
        publishes_item.setExpanded(True)
        
        if wips:
            wip_table_item = QTreeWidgetItem(working_item)
            wip_table = QTableWidget()
            self.initialize_table_widget(wip_table)
            self.ui.treeWidget_grid_total.setItemWidget(wip_table_item, 0, wip_table)
            self.fill_table_with_data(wip_table, wips, versions, thumbnail_list, 'wip')

        if pubs:
            pub_table_item = QTreeWidgetItem(publishes_item)
            pub_table = QTableWidget()
            self.initialize_table_widget(pub_table)
            self.ui.treeWidget_grid_total.setItemWidget(pub_table_item, 0, pub_table)
            self.fill_table_with_data(pub_table, pubs, versions, thumbnail_list, 'pub')

    def set_file_table_list(self, filter):  # WIP 및 Pub 파일을 나누어 보여주기 ★
        """
        WIP 및 Pub 파일을 나누어 보여주는 함수입니다.
        """
        # 테이블 위젯 초기화
        self.ui.tableWidget_list_pub.clear()
        self.ui.tableWidget_list_wip.clear()
        
        # 탭 위젯 파일 갯수 초기화
        self.ui.tabWidget_file_list.setTabText(1, 'Working')
        self.ui.tabWidget_file_list.setTabText(2, 'Publishes')
        

        # 필터에 따라 선택된 항목 가져오기
        if filter == 'my_task_signal':
            selected_item = self.ui.treeWidget_my_tasks.currentItem()
        elif filter == 'asset_signal':
            selected_item = self.ui.treeWidget_assets.currentItem()
        elif filter == 'shot_signal':
            selected_item = self.ui.treeWidget_shots.currentItem()

        # 선택된 항목 확인
        if selected_item is None or selected_item.childCount() != 0:
            return

        # 선택된 항목에서 정보 가져오기
        task_id = selected_item.data(0, Qt.UserRole)
        wips, pubs, versions = self.get_version(task_id)

        # 테이블 위젯 설정
        self.initialize_table_widget(self.ui.tableWidget_list_wip)
        self.initialize_table_widget(self.ui.tableWidget_list_pub)

        # 썸네일 리스트 한 번만 호출
        thumbnail_list = self.get_thumbnail_list(task_id)

        # WIP와 Pub 데이터를 테이블 위젯에 채우기
        if wips:
            self.fill_table_with_data(self.ui.tableWidget_list_wip, wips, versions, thumbnail_list, 'wip')

        if pubs:
            self.fill_table_with_data(self.ui.tableWidget_list_pub, pubs, versions, thumbnail_list, 'pub')
        
    """
    하단 레이어 셋팅
    """
    def setup_bottom_layer(self):   # 하단 레이어 셋팅
        self.set_new_file_name()
        self.set_new_file_ver()
        self.set_file_type()
        self.set_preview()
        self.set_work_area()
        
        if not self.check_right_entity():
            self.ui.label_validate_path.setText('■ The save path is not valid.')
        else: 
            self.ui.label_validate_path.clear()
            
    def set_new_file_name(self):    # 파일 이름 정보 띄워주기
        file_name_with_ver = os.path.basename(current_path)
        now_version = self.check_file_version()
        file_name = file_name_with_ver.split(f"_{now_version}")[0]
        self.ui.label_new_file_name.setText(file_name)
        return file_name
    
    def set_new_file_ver(self): # 버전 정하기
        _, next_version = self.check_shotgrid_version()
        
        if self.ui.checkBox_avaliable_ver.isChecked():
            self.ui.spinBox_version.setValue(int(next_version))
            version = f"v{next_version}"
            self.ui.spinBox_version.setEnabled(False)
        else:
            self.ui.spinBox_version.setEnabled(True)
            changed_version = self.ui.spinBox_version.value()
            version = f"v{str(changed_version).zfill(3)}"
        return version
    
    def set_file_type(self):    # 열린 프로그램 기준 파일 확장자 정하기
        # 누크일 때, 마야일 때 분리(프로그램별 상이)
        self.ui.comboBox_filetype.clear()
        
        maya = ["ma", "mb"]
        nuke = ["nk", "nknc"]
        if self.check_file_type() in maya:
            self.ui.comboBox_filetype.addItems(maya)
            self.ui.comboBox_filetype.setCurrentText("mb")
        elif self.check_file_type() in nuke:
            self.ui.comboBox_filetype.addItems(nuke)
            self.ui.comboBox_filetype.setCurrentText("nk")
            
    def set_preview(self):  # 저장될 파일 이름 미리 보여주기
        file_name = self.set_new_file_name()
        ver = self.set_new_file_ver()
        ext = self.ui.comboBox_filetype.currentText()
        new_file_name = f"{file_name}_{ver}.{ext}"
        self.ui.label_preview.setText(new_file_name)
        
        return new_file_name
        
    def set_work_area(self):    # 저장될 경로 미리 보여주기
        # 선택이 안됐을 때 경로 정하기
        # 선택이 됐을 때 경로 정하기 
        extracted_path,_ = self.get_shotgrid_directory()
        new_file_name = self.set_preview()
        work_area = f"{extracted_path}/{new_file_name}"
        self.ui.label_work_area.setText(work_area)
        self.store_save_info()
    
    """
    기타
    """
    def close_ui(self): # 프로그램 닫기
        self.close()
    
    def change_current_path(self, filter):  # 저장될 경로 바꾸기
        global current_path
        root_path = f'{self.root_path}/phoenix_pipeline_folders/'
        
        # 필터에 따라 선택된 항목 가져오기
        if filter == 'my_task_signal':
            selected_item = self.ui.treeWidget_my_tasks.currentItem()
            
        elif filter == 'shot_signal':
            selected_item = self.ui.treeWidget_shots.currentItem()
            entity = 'Shots'
            
        elif filter == 'asset_signal':
            selected_item = self.ui.treeWidget_assets.currentItem()
            entity = 'Assets'
        
        # 선택된 항목 확인
        if selected_item is None:
            return
        if not selected_item.childCount() == 0:
            return
        if selected_item.parent().parent() == None:
            return
        
        if filter == 'my_task_signal':
            entity = selected_item.parent().parent().text(0)
        
        # 선택된 항목에서 정보 가져오기
        task_id = selected_item.data(0, Qt.UserRole)
        task_info = self.get_task_related_info(task_id)
        
        if entity ==  'Shots':
            new_current_path_without_ext = os.path.join(root_path,task_info['project_name'],
                                            entity,task_info['sequence_name'],
                                            task_info['shot_name'],task_info['task_name'],
                                            "wip",task_info['latest_version'])
        elif entity == 'Assets':
            new_current_path_without_ext = os.path.join(root_path,task_info['project_name'],
                                            entity,task_info['asset_type'],
                                            task_info['asset_name'],task_info['task_name'],
                                            "wip",task_info['latest_version'])
            
        ext = self.initial_path.split('.')[-1]
        new_current_path = f"{new_current_path_without_ext}.{ext}"
        current_path = new_current_path
        self.store_changed_path()
        self.setup_bottom_layer()
        
    def make_save_local_path(self): # 로컬에 저장할 경로 만들기
        save_info, entity_type = self.store_save_info()
        
        root_path = f"{self.root_path}/phoenix_pipeline_folders/"
        project_name = save_info['project']['name']
        if entity_type == "Shots":
            seq_name = save_info['sequence']['name']
            shot_name = save_info['shot']['name']
            task_name = save_info['task']['name']
            file_name = self.set_preview()
            
            local_path = os.path.join(root_path,project_name,entity_type,
                                      seq_name,shot_name,task_name,
                                      "wip",file_name)
            
        elif entity_type == "Assets":
            asset_type_name = save_info['asset_type']['name']
            asset_name = save_info['asset']['name']
            task_name = save_info['task']['name']
            file_name = self.set_preview()
        
            local_path = os.path.join(root_path,project_name,entity_type,
                                      asset_type_name,asset_name,task_name,
                                      "wip",file_name)
        return local_path
    
    def save_file(self):    # 로컬에 파일을 저장하고 샷그리드로 링크 걸어주기
        if not self.check_right_entity():
            return print('저장할 경로를 다시 확인해주세요.')
        project_id = self.get_project_id()
        user_id = self.get_user_id()
        file_saver = FileSaver()
        file_path = self.make_save_local_path()
        # 로컬에 파일 저장하기
        ext = current_path.split('.')[-1]
        if ext in ['nk', 'nknc']:
            file_saver.save_in_local('Nuke', file_path)
            # 샷그리드에 파일경로 업로드
            save_info, entity_type = self.store_save_info()
            created_ver_id = file_saver.upload_to_shotgrid(save_info, entity_type, file_path, ext, user_id)
            # 새로운 데이터 정보 반영해서 UI 업데이트
            self.explorer_json.update_version_json(project_id, created_ver_id, save_info, entity_type)
            self.initial_path = current_path
            self.first_show()
            self.show_current_path_tree()
            
        elif ext in ['ma', 'mb']:
            file_saver.save_in_local('Maya', file_path)
            # 샷그리드에 파일경로 업로드
            save_info, entity_type = self.store_save_info()
            created_ver_id = file_saver.upload_to_shotgrid(save_info, entity_type, file_path, ext, user_id)
            # 새로운 데이터 정보 반영해서 UI 업데이트
            self.explorer_json.update_version_json(project_id, created_ver_id, save_info, entity_type)
            self.initial_path = current_path
            self.first_show()
            self.show_current_path_tree()
        
    def find_root_path(self):   # 현재 컴퓨터의 기본 주소를 받습니다.
        self.root_path = os.path.expanduser('~')
    
    def center(self):   # 창 가운데 띄우기
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        new_top_left = qr.topLeft()
        # new_top_left -= QPoint(300, 120)
        self.move(new_top_left)
    
             
    def setting(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        """
        UI 표시 셋팅 
        """
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)   # 항상 위에 띄우기
        
        # 창을 화면 중앙에 띄우기
        self.center()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SaverUIHandler()
    win.show()
    sys.exit(app.exec())
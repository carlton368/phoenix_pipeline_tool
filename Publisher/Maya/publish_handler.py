import os
import sys
import re
print("publish_handler!!")
sys.path.append("/home/rapa/_phoenix_/lib/site-packages")
from importlib import reload
from shotgun_api3 import Shotgun
from functools import partial
import json

try:
    from PySide6.QtWidgets import *
    from PySide6.QtWidgets import QWidget
    from PySide6.QtUiTools import *
    from PySide6.QtCore import *
    from PySide6.QtGui import *
except:
    from PySide2.QtWidgets import *
    from PySide2.QtWidgets import QWidget
    from PySide2.QtUiTools import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    
# from ui.ui_publisher import Ui_Form
    
from Publisher.Maya.get_maya_current_path import MayaCurrentPathImporter
from Publisher.Maya.maya_pub_data_manager import MayaOutlinerInfoCatcher,MayaFileSaver

from Publisher.Maya.maya_messageBox import MayaMessageBoxPrompter
from Publisher.Maya.maya_playblast_scene_setter import PlayblastSceneSetter
from Publisher.Maya.data_explorer_sj import DataExplorer
from Publisher.Maya.ValidationCheckForMaya import ValidateByTask, ValidationCheckForMaya

# from Publisher.Maya.publish_data_to_shotgrid import PublishDataToShotGrid


class PublishHandler(QMainWindow,DataExplorer):
    def __init__(self):
        super().__init__()
        self.root_path = "/home/rapa"
        # self.ui = Ui_Form()
        # self.ui.setupUi(self)
        self.set_information()
        self.setting()
        self.first_show()
        self.selected_items = self.get_outliner_items()
        # self.data_explorer = DataExplorer()
        self.infocatcher = MayaOutlinerInfoCatcher()
        self.file_saver = MayaFileSaver()
        self.publish_button_event()  
        self.outliner_warning()
        print("self.version",self.version)
        # screen = MakeScreenCaptureeeeee(self.ui)#열자마자 해당 샷의 버젼이 샷그리드에 올라와 있는지 체크.. 만약 없다면 세이브 부터
        ####################################################################################################################
        self.cache_path = False
        self.camera_path = False
        self.pub_path = self.get_publish_path()
        
        print("1",self.pub_path)
        
    def set_information(self):
        self.sg = Shotgun(
            "https://4thacademy.shotgrid.autodesk.com/",  
        script_name = "kangseyoung",
        api_key = "imthtqts8zqqXylfckoiihx-z")
        self.selected_items = []
        self.infocatcher = MayaOutlinerInfoCatcher()
        self.file_saver = MayaFileSaver()
        maya_importer = MayaCurrentPathImporter()
        self.path = maya_importer.show_file_path()
        self.version = self.check_existence_of_version()
        self.task_step = self.get_user_task()
        self.validate_checker = ValidateByTask()
        self.validate_checklist = self.validate_checker.check_validation_list_for_task(self.task_step)
        print(self.validate_checklist)
        
        
    def setting(self):
        ui_file_path = "/home/rapa/_phoenix_/ui/publisher.ui" 
        ui_file = QFile(ui_file_path)
        print("settings..")
        self.ui = QUiLoader().load(ui_file, self) # UI 파일 로드 후 파일 닫기'
        self.label_thum_img = self.ui.findChild(QLabel,"label_thum_img")
        # UI 파일 로드 후 파일 닫기
        # Screen_Capture 객체 생성 시 parent로 self.ui를 설정
        QTimer.singleShot(0, self.make_screenshot)
        self.capture = Screen_Capture(self.ui.label_thum_img, parent=self.ui)
        
    def closeEvent(self, event):
        # UI창이 닫힐 때 호출되는 메서드
        if hasattr(self, 'capture') and self.capture:
            self.capture.close()  # Screen_Capture 객체 종료
        QApplication.restoreOverrideCursor()  # 커서 상태 복원
        event.accept()  # 창 닫기 이벤트를 받아들임    
        
    def publish_button_event(self): 
            
        self.ui.pushButton_publish.clicked.connect(self.collect_selected_files)
        
    def validation_button_event(self):
        
        self.ui.pushButton_validate.clicked.connect(self.validate)
        
        
    def validate(self):
        """
        여기에 validation 추가해주시면 됩니다.
        """
        
        pass
    ####################################################################################
    
    def get_project_id_one(self):   # 프로젝트 데이터 가져오기 
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
    ########################################################################################
    def get_user_task(self):  #  세영 추가 version 정보에서 taskid  추출 후, task step 대한 정보를 가져옵니다
        
        try:
            # Task 엔터티를 가져옵니다.
            task_entity_in_version = self.version.get("sg_task")
            if not task_entity_in_version:
                print("버전에서 Task 엔터티를 가져올 수 없습니다.")
                return None
            
            # Task ID를 가져옵니다.
            task_id = task_entity_in_version.get("id")
            if not task_id:
                print("Task 엔터티에서 Task ID를 가져올 수 없습니다.")
                return None
            print(f"Task ID: {task_id}")
            # Task ID로 Task Step을 가져옵니다.
            task_step = self.get_task_step_by_id(task_id)
            print("task_step:",task_step)
            if not task_step:
                print("Task ID에서 Task Step을 가져올 수 없습니다.")
                return None
            # self.ui.label_des_context.setText(task_step)
            print(f"Task Step: {task_step}")
            return task_step

        except AttributeError as e:
            print(f"AttributeError 발생: {e}")
            return None
        except KeyError as e:
            print(f"KeyError 발생: {e}")
            return None
        except Exception as e:
            print(f"예기치 않은 오류 발생: {e}")
            return None
 
    # ui에 정보를 띄우는 부분
    def first_show(self): #self.path 설정 #마야이면, 마야 경로가, 누크면 누크 경로가 세팅된다.
        project_id = self.get_project_id_one()
        user_id = self.get_user_id()
        self.project_name = self.get_project_name(project_id)
        print(project_id,user_id)
        self.ui.label_username.setText(self.get_user_name(user_id))
        self.ui.label_project_name.setText(self.get_project_name(project_id))
        
        self.tree_widget = self.ui.findChild(QTreeWidget, "treeWidget_main")
        self.label_file_name = self.ui.findChild(QLabel, "label_file_name")
        self.label_icon = self.ui.findChild(QLabel, "label_icon")
        self.label_file_type = self.ui.findChild(QLabel, "label_file_type")
        self.text_description = self.ui.findChild(QTextEdit, "text_description")
        
        self.load_file(self.path)
        
        if self.tree_widget.topLevelItemCount() > 0:
            first_item = self.tree_widget.topLevelItem(0)
            self.tree_widget.setCurrentItem(first_item)
            self.get_file_info(first_item, 0)
            
        self.tree_widget.itemClicked.connect(self.get_file_info)

    def load_file(self, *file_paths): #파일 이름을 ui에 개시
        """
        ui에 파일에 관련한 정보를 게시합니다.
        파일 명 및 아웃라이너 오브젝트들 정보
        """
        
        
        for file_path in file_paths:
            if os.path.exists(file_path) and file_path.endswith(('.mb', '.ma', '.nknc', '.nk')):
                file_name = os.path.basename(file_path)
                tree_item = QTreeWidgetItem(self.tree_widget)
                tree_item.setText(0, file_name)
                tree_item.setToolTip(0, file_path)
                tree_item.setExpanded(True)
                
                # 리스트가 두 개일 경우와 한 개일 경우 존재함
                # 룩뎁과 라이팅의 경우 한 번 더 넣어줘야함
                i = self.get_outliner_items()
                if i:
                    self.add_outliner_items(tree_item,i,"Outliner") ################수정
                self.add_outliner_items(tree_item,self.validate_checklist,"Validation List")
                    
    
    def get_file_info(self, item, column): #파일의 type을 ui에 띄운다
        selected_file_name = item.text(column)
        self.label_file_name.setText(selected_file_name)
        
        file_extension = os.path.splitext(selected_file_name)[-1].lower()
        if file_extension in ['.mb', '.ma']:
            pixmap = QPixmap("/home/rapa/backup/_phoenix_/ui/image_source/maya.png")
            file_type = "Maya Session"
        elif file_extension in ['.nk', '.nknc']:
            pixmap = QPixmap("/home/rapa/backup/_phoenix_/ui/image_source/Nuke.png")
            file_type = "Nuke Session"
        else:
            pixmap = QPixmap()
            file_type = "Unknown File Type"

        self.label_icon.setPixmap(pixmap)
        self.label_icon.setScaledContents(True)
        self.label_file_type.setText(file_type)

    def sync_checkboxes(self, state, checkboxes): #check 박스의 상태를 세팅해줌
        for checkbox in checkboxes:
            checkbox.setCheckState(Qt.CheckState(state))

    def collect_selected_files(self):# 트리의 모든 항목을 확인하여 체크된 항목을 새 씬에 저장하고, ShotGrid에 업로드 #수정한 부분 #push 버튼 누르면 넘어간다..
        
        # root = self.tree_widget.invisibleRootItem()
        # child_count = root.childCount()

        # for i in range(child_count):
        #     item = root.child(i)
        #     file_path, checkbox = item.data(0, Qt.UserRole)
            
        #     if checkbox.isChecked():
        #         self.upload_to_shotgrid(self.version) #샷그리드 업로드 함수로 감
        self.upload_to_shotgrid()
        
    def outliner_warning(self):
        self.task_step = self.get_user_task()
        print("outliner_warning",self.task_step)
        warn_list_task = ['rig','mod']
        if self.task_step in warn_list_task:
            count_objects = 0
            for item in self.get_outliner_items():
                print(item)
                count_objects += 1
            if count_objects > 1:
                self.ui.label_validation_error.setText("There are more than two objects in the Outliner.")
                self.ui.label_validation_error.setStyleSheet("""
                QLabel {
                    color: #e74c3c; /* 텍스트 색상: 빨간색 */
                    background-color: #f9e6e6; /* 배경색: 부드러운 빨간색 */
                    border: 2px solid #e74c3c; /* 테두리: 빨간색 */
                    border-radius: 1px;
                    padding: 5px;
                    font-size: 12px;
                    font-weight: bold;
                    text-align: center;
                }
            """)
    ########################################################################################
    
    def check_existence_of_version(self):
        """
        현재 샷에
        파일이름을 통해 할당된 task와, entity를 가져옵니다.
        publish 버젼이 있는지 샷그리드에서 조회합니다.
        """
        project_id = self.get_project_id_one()
        print(project_id)
        basename = os.path.basename(self.path) #파일의 경로를 넣어, 파일 이름 찾기
        name = basename.split(".")
        file = name[0] #파일 이름 가지고 검색중,,mb떼고..
        print(file)
        version = self.sg.find_one('Version', [['project.Project.id', 'is', project_id],['code', 'is', file]], ['sg_task','entity']) #현재 파일의 version을 찾음 없으면, 메시지 띄우기,z
        print(version)
        
        if isinstance(version, dict):
            self.find_version_number(version)
            
            return version
        
        if not version:
            m = MayaMessageBoxPrompter()
            m.show_version_not_saved_warning()
            print("저장된 버젼 없음..")
            return None
    ######################################################################################
        
    def upload_to_shotgrid(self): #basename으로 뒤에 확장자 떼고, 버젼 찾기 버젼에 할당된 태스크 찾아서 그 태스크의 버젼들 갯수 세서 제일 최근 버젼
        """
        

        """
        
        self.save_checked_data()
        
        print("#"*10)
        #get_slate_path 하나 만들기
        # if self.task_step == "mod":z
        #     maya_slate_path = self.file_saver.asset_make_slate(self.pub_path, self.get_project_name())
        #     self.file_saver.set_freeze()
            
        
        # if self.task_step in ['rig','lkd']:
        #     maya_slate_path = self.file_saver.asset_make_slate(self.pub_path, self.get_project_name())
            
            
        # elif self.task_step == ["ani"]:
        #     maya_slate_path = self.file_saver.shot_make_slate(self.pub_path, self.get_project_name())
            
        # elif self.task_step == "mm":
        #     maya_slate_path = self.file_saver.shot_make_slate(self.pub_path, self.get_project_name())
        #     width, height = self.infocatcher.get_render_resolution()
        #     print(width, height)
        
        # elif self.task_step == "lgt":
        #     #slate 없고, exr만 펍 되면 됨.
        #     self.file_saver.render_exr()
        #     self.file_saver.save_selected_items_as_mb(self.selected_items,self.pub_path)

        print("#"*10)
        print("self.pub_path는..",self.pub_path)
        published_file_type = self.sg.find_one("PublishedFileType", [["code", "is", "Maya Scene"]], ["id"])
        if not published_file_type:
                print("'Maya Scene'이 없습니다.")
                return
        print(self.pub_path)
        user_id = self.get_user_id()
        if self.pub_path:
            pub_file = os.path.basename(self.pub_path)
            print(pub_file)
            code = pub_file.split(".")[0]
            task = self.version.get("sg_task")
            task_id = task.get("id")
            entity = self.version.get('entity')
            entity_id = entity.get('id')
            entity_type = entity.get('type')
            

            
        #[{'type': 'Version', 'id': 7687, 'sg_task': {'id': 6869, 'name': 'teapot_mod_v001 Task', 'type': 'Task'}, 'entity': {'id': 1735, 'name': 'teapot_mod_v001', 'type': 'Asset'}}]
        
        
        if self.task_step == "lkd":
            
            maya_slate_path = self.file_saver.rig_make_slate(self.pub_path, self.project_name)
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 191},
            'sg_path': self.ma_path, #이게 두번 올라감..?
            'sg_status_list': 'pub', #user 정보 올라가야함
            'sg_shader_json_path': f"{self.json_path}",
            'sg_version_file_type': published_file_type,
            "user": {"type": "HumanUser", "id": user_id}
            
            })
            published_file_type = self.sg.find_one("PublishedFileType", [["code", "is", "Maya Scene"]], ["id"])
            if not published_file_type:
                print("'Maya Scene'이 없습니다.")
                return
            
            created_published_file = self.sg.create("PublishedFile",{
                "project": {"type": "Project", "id": 191},
                "entity": entity,
                "task": {"type": "Task", "id": task_id}, 
                "path": {"local_path": self.ma_path}, 
                "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사용
                'path_cache':self.json_path,
                'sg_status_list':'ip',
                'published_file_type': published_file_type,
                'code': f'{code}'
            })
                        

                
        #리깅일 경우.. mb 파일로만 나감
        elif self.task_step == "rig":
            maya_slate_path = self.file_saver.rig_make_slate(self.pub_path, self.project_name)
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 191},
            'sg_path': self.pub_path,
            'sg_status_list': 'pub', #user 정보 올라가야함,
            'sg_version_file_type': published_file_type,
            "user": {"type": "HumanUser", "id": user_id}
            
                
            })
            
            created_published_file = self.sg.create("PublishedFile",{
                    
                    "project": {"type": "Project", "id": 191},
                    "entity": entity,
                    "task": {"type": "Task", "id": task_id}, 
                    "path": {"local_path": self.pub_path}, 
                    "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사
                    'published_file_type': published_file_type,
                    'code': f"{code}"
            })   
            
        elif self.task_step == "mod":
            maya_slate_path = self.file_saver.asset_make_slate(self.pub_path, self.project_name)
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 191},
            'sg_path': self.mb_path,
            'sg_status_list': 'pub', #user 정보 올라가야함   
            'sg_cache_path':f"{self.cache_path}",
            'sg_version_file_type': published_file_type
            
        })
            created_published_file = self.sg.create("PublishedFile",{
                
                "project": {"type": "Project", "id": 191},
                "entity": entity,
                "task": {"type": "Task", "id": task_id}, 
                "path": {"local_path": self.mb_path }, 
                "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사용
                'path_cache':f"{self.cache_path}",
                'published_file_type': published_file_type,
                'code': f"{code}"
            })
            
        elif self.task_step == "lgt":
            
            created_published_file = self.sg.create("PublishedFile",{
                    
                    "project": {"type": "Project", "id": 191},
                    "entity": entity,
                    "task": {"type": "Task", "id": task_id}, 
                    "path": {"local_path": self.pub_path}, 
                    "description": self.ui.description.toPlainText(),   #UI에 입력된 desmaya_slate_pathcription 사
                    'published_file_type': published_file_type,
                    'code': f"{code}"
            })   
            return created_published_file
            
        elif self.task_step == "ani": # 만약에 anim_cam 이 있다면, 카메라 캐쉬 나가주게 짜야함,
            maya_slate_path = self.file_saver.shot_make_slate(self.pub_path, self.project_name)
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 191},
            'sg_path': self.pub_path,
            'sg_status_list': 'pub', #user 정보 올라가야함   
            'sg_cache_path':f"{self.cache_path}",
            'sg_version_file_type': published_file_type,
            "user": {"type": "HumanUser", "id": user_id}
            
        })
            created_published_file = self.sg.create("PublishedFile",{
                
                "project": {"type": "Project", "id": 191},
                "entity": entity,
                "task": {"type": "Task", "id": task_id}, 
                "path": {"local_path": self.pub_path }, 
                "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사용
                'path_cache':f"{self.cache_path}",
                'published_file_type': published_file_type,
                'code': f"{code}"
                
            })
            
        elif self.task_step == "mm": #카메라 캐쉬 나가줘야하나?
            maya_slate_path = self.file_saver.shot_make_slate(self.pub_path, self.project_name)
            width, height = self.infocatcher.get_render_resolution()
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 191},
            'sg_path': self.pub_path,
            'sg_status_list': 'pub', #user 정보 올라가야함   
            'sg_cache_path':f"{self.cache_path}",
            'sg_version_file_type': published_file_type,
            "user": {"type": "HumanUser", "id": user_id}
        })
            created_published_file = self.sg.create("PublishedFile",{
                "project": {"type": "Project", "id": 191},
                "entity": entity,
                "task": {"type": "Task", "id": task_id}, 
                "path": {"local_path": self.pub_path }, 
                "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사용
                'path_cache':f"{self.cache_path}",
                'published_file_type': published_file_type,
                'code': f"{code}"
                
            })
            self.update_undistortion_size_camera_path(entity_id, width, height)
        # self.selected_items += "rt_gr"
        # self.save_checked_data()
            
            
        print(f"{created_published_file['id']}가 퍼블리쉬 되었습니다.")  
            
        print(self.pub_path)
        print(new_version)
        print("version_created")
                
        version_id = new_version.get("id")
        version_code = new_version.get("code")
        slate_path = maya_slate_path
        print("slate_path",slate_path)
        self.sg.upload("Version",version_id, slate_path, field_name= "sg_uploaded_movie")
        
        print(f"{version_code} 슬레이트가 업로드되었습니다.")    
               
    def update_undistortion_size_camera_path(self,shot_id,width,height):
        if not self.camera_path:
        
            update_data = {'sg_undistortion_width':width ,
                'sg_undistortion_height': height
            }
            shot_updated = self.sg.update("Shot", shot_id, update_data)
            print(shot_updated)
            
        update_data = {'sg_undistortion_width':width ,
                    'sg_undistortion_height': height, 
                    'sg_camera_cache_path' : self.camera_path
                }
        shot_updated = self.sg.update("Shot", shot_id, update_data)
        print(shot_updated)     
                       
    def add_outliner_items(self, parent_item, outliner_items , label_text): #아웃라이너 ui에 추가
        
        frame2 = QFrame()
        layout2 = QHBoxLayout(frame2)

        label2 = QLabel(label_text)
        label2.setStyleSheet("QLabel { color: #ffffff; font-size: 18px; }"
                             
                             )
        label2.setContentsMargins(20, 0, 0, 0)
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout2.addWidget(label2)
        layout2.addItem(spacer2)
        layout2.setAlignment(Qt.AlignLeft)
        layout2.setContentsMargins(0, 0, 20, 0)
        details_item2 = QTreeWidgetItem(parent_item)
        self.tree_widget.setItemWidget(details_item2, 0, frame2)

        self.add_outliner_toggle(details_item2, outliner_items,label_text)
        
        details_item2.setExpanded(True)


    def add_outliner_toggle(self, parent_item, texts, label): #아웃라이너에 있는 아이템을 ui에 추가 
        
        if label == "Validation List":
            for text in texts:
                frame = QFrame()
                layout = QHBoxLayout(frame)
                label = QLabel(text)
                label2 = QLabel(text)
                label.setContentsMargins(0, 0, 0, 0)

                light = QPixmap("/home/rapa/_phoenix_/ui/image_source/")
                resized_pixmap = light.scaled(10, 10)
                label2.setPixmap(resized_pixmap)
                spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

                layout.addWidget(label)
                layout.addItem(spacer)
                layout.addWidget(label2)
                # layout.addWidget(light)
                layout.setAlignment(Qt.AlignLeft)
                layout.setContentsMargins(0, 0, 20, 0)

                # checkbox.clicked.connect(partial(self.select_outliner_items,light,text))
                label.setStyleSheet("QLabel { font-size: 15px; }"
                                
                                )
                sub_item = QTreeWidgetItem(parent_item)
            
                self.tree_widget.setItemWidget(sub_item, 0, frame)
               
        else:
            for text in texts:
                frame = QFrame()
                layout = QHBoxLayout(frame)
                label = QLabel(text)
                label.setContentsMargins(0, 0, 0, 0)

                checkbox = QCheckBox()
                spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

                layout.addWidget(label)
                layout.addItem(spacer)
                layout.addWidget(checkbox)
                layout.setAlignment(Qt.AlignLeft)
                layout.setContentsMargins(0, 0, 20, 0)
                
                checkbox.setChecked(True)
                self.selected_items.append(text)
                checkbox.clicked.connect(partial(self.select_outliner_items,checkbox,text))
                label.setStyleSheet("QLabel { font-size: 15px; }"
                                
                                )
                sub_item = QTreeWidgetItem(parent_item)
            
                self.tree_widget.setItemWidget(sub_item, 0, frame)
                
    def get_outliner_items(self):
        node_catcher = MayaOutlinerInfoCatcher()
        if self.task_step == "mod":
            node_except_cameras = node_catcher.get_filtered_and_simplified_objects()
            return node_except_cameras
        elif self.task_step == "rig":
            node_except_cameras = node_catcher.get_filtered_and_simplified_objects()
            return node_except_cameras
        elif self.task_step == "lkd":
            node_except_cameras = node_catcher.get_filtered_and_simplified_objects()
            # used_materials = node_catcher.get_list_used_materials()
            return node_except_cameras
        elif self.task_step == "ani":
            node_except_cameras = node_catcher.get_filtered_and_simplified_objects()
            return node_except_cameras
        elif self.task_step == "mm":
            node_except_cameras = node_catcher.get_filtered_and_simplified_objects()
            return node_except_cameras
        elif self.task_step == "lgt":
            node_except_cameras = node_catcher.get_filtered_and_simplified_objects()
            render_layers =  node_catcher.get_all_layers()
            return render_layers
    
    def select_outliner_items(self,checkBox,text):#아웃라이너의 아이템들을 선택하고 텍스트를 반환합니다 #
        
        if checkBox.isChecked():
            selected_item = text
            if selected_item in self.selected_items:
                self.selected_items.remove(f"{selected_item}")
            self.selected_items.append(selected_item)
        if not checkBox.isChecked():
            selected_item = text
            self.selected_items.remove(f"{selected_item}")  
        print(f"{self.selected_items}가 선택되었습니다.")
        return self.selected_items
    
    def save_checked_data(self): #선택된 모델들의 텍스트를 활용해 펍합니다.
        
        print("file_saver 실행중..")
        self.mayafilesaver =  MayaFileSaver()
        cache_data_task = ["mod", "ly", "mm","ani","cmp"]
        print("task_Step은..",self.task_step)
        if not self.selected_items: #self.selected_items
            return print("Publish 할 아이템을 선택해주세요.")
        if not self.pub_path:
            print(self.pub_path)
            return print("Publish 할 경로가 지정되지 않았습니다.")
        
        if self.task_step == "lkd":
            self.json_path, self.ma_path = self.mayafilesaver.export_shader_ma_json(self.pub_path)
            print(self.json_path,self.ma_path)
            
        elif self.task_step == "lgt":
            print("saving lgt...")
            aovs = self.get_standard_aov_info(191)################################################수정해야함
            print("aovs",aovs)
            cache_mb_exr_path = self.get_version_dir(self.pub_path)
            self.exr_path = self.mayafilesaver.render_exr(cache_mb_exr_path,self.pub_path,aovs, self.selected_items)
            print("exr_path")
            self.mb_path = self.mayafilesaver.save_selected_items_as_mb(self.get_outliner_items(), self.pub_path)
            print( self.exr_path, self.mb_path)
            
        elif self.task_step == "rig":
            
            self.mayafilesaver.save_selected_items_as_mb(self.selected_items, self.pub_path)
            print(self.selected_items)
            print(self.pub_path)
            
            
        elif self.task_step == "mm": #mm의 카메라 캐쉬 경로가 export 되어야함.
            cache_mb_path = self.get_version_dir(self.pub_path)
            print(cache_mb_path)
            self.cache_path, self.mb_path = self.mayafilesaver.export_selected_items_as_alembic_and_mb(self.selected_items,cache_mb_path,self.pub_path)
            self.camera_path = self.get_camera_cache_path(self.cache_path)
            
    
            
        elif self.task_step == "ani": # mm의 카메라가 있을 경우, mm의 카메라가 없을 경우.
            cache_mb_path = self.get_version_dir(self.pub_path)
            print(cache_mb_path)
            self.cache_path, self.mb_path = self.mayafilesaver.export_selected_items_as_alembic_and_mb(self.selected_items,cache_mb_path,self.pub_path)
            self.camera_path = self.get_camera_cache_path(self.cache_path)
            
            print(self.selected_items)
            
        elif self.task_step in cache_data_task:
            cache_mb_path = self.get_version_dir(self.pub_path)
            print(cache_mb_path)
            self.cache_path, self.mb_path = self.mayafilesaver.export_selected_items_as_alembic_and_mb(self.selected_items,cache_mb_path,self.pub_path)
            print(self.selected_items)
            
        return self.pub_path, self.selected_items 
        
    def get_publish_path(self):
        import re
        pattern = r'v(\d{3})'
        new_version_number = self.find_version_number(self.version)
        new_path = self.path.replace("wip","pub")
        # 새 버전 번호 추가
        if 'v' in new_path:
            new_path = re.sub(pattern, f'v{new_version_number}', new_path)  # 처음 나오는 'v'에만 새 버전 번호 추가
        print(new_path)
        return new_path
        
    
    def get_version_dir(self,pub_path):
        import re
        new_version_number = self.find_version_number(self.version)
        self.project_name = self.get_project_name(self.get_project_id_one())
        dir_path = os.path.dirname(pub_path) #pubpath의 경로
        print("dir_path",dir_path)
        # 정규표현식을 사용해 프로젝트 이름 뒤에 'cache'를 삽입
        pattern = rf"({self.project_name})(/)"
        print("projectname",self.project_name)
        
        cache_dir = re.sub(pattern, r"\1/cache\2", dir_path) 
        print("cache_dir",cache_dir)#경로에 cache 추가됨
        
  
        return cache_dir
               
    def find_version_number(self,version):
        ##################################################################### #여기 수정해야함  #버젼 넘버를 버젼 체크한 다음에 가져와야할듯
        """
        

        Args:
            version (dict): version entity

        Returns:
            str: version_number
        version entity에서 해당 파일의 이름으로 code 검색 후, 
        pub 상태인 것들중, 가장 높은 숫자의 번호를 가져옴
        """
        task = version['sg_task'] #얠 입력하면, 버젼별 이름이 나오게끔..
        pub_versions = self.get_pub_version_code(task)
        if not pub_versions:
            new_version_number = str(int(1)).zfill(3)
            return new_version_number
        version_codes = []
        pattern = r'v(\d{3})'
        for version in pub_versions:
            version_code = version.get("code")
            match = re.search(pattern, version_code)
            int_match = match.group(1) #001 v떼고
            version_codes.append(int_match)
            # 정규 표현식 패턴 #pub된 것들 버젼 다 가져오기
        sort = sorted(version_codes)
        print("find_version_number sort",sort)
        code = sort[-1]
        new_version_number = str(int(code)+1).zfill(3)
        print(new_version_number)
        return new_version_number
    
    def make_screenshot(self):
        self.capture = Screen_Capture(self.label_thum_img)
        self.capture.show()
     
    def get_camera_cache_path(self, abc_paths):
        for abc_path in abc_paths:
            if "camera" in os.path.basename(abc_path):
                return abc_path

        
        
##################################################################################################
class Screen_Capture(QWidget):

    def __init__(self, label_thum_img, parent=None):
        super().__init__(parent)

        self.start_pos = None
        self.end_pos = None
        self.label_thum_img = label_thum_img

        QApplication.setOverrideCursor(Qt.CrossCursor) # 커서 오버라이드
        self.setWindowFlag(Qt.FramelessWindowHint) # 투명 윈도우인데 위에 제목표시줄 있으면 안되서 지우는 부분
        self.setWindowOpacity(0.3) # 윈도우 투명도 0.3
        self.setAttribute(Qt.WA_TranslucentBackground) # 투명도를 쓰겠다는 명령어
        self.showFullScreen() # 풀스크린 위젯
        
    def mousePressEvent(self, event):
        """
        마우스를 눌렀을때 발생하는 이벤트
        """
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = self.start_pos
            self.update()
    
    def mouseMoveEvent(self, event):
        """
        마우스를 움직일때 발생하는 이벤트 
        """
        if self.start_pos:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """
        마우스 왼쪽 버튼을 땠을때 발생하는 이벤트
        """
        if event.button() == Qt.LeftButton:
            self.end_pos = event.pos()
            self.capture_screen()
            QApplication.restoreOverrideCursor()
            self.start_pos = None
            self.end_pos = None
            self.close()

    def capture_screen(self):
            """
            실제로 화면을 캡쳐하는 메서드
            """
            if self.start_pos and self.end_pos:
                x = min(self.start_pos.x(), self.end_pos.x())
                y = min(self.start_pos.y(), self.end_pos.y()) # X, Y는 드래그된 마우스 포인터의 좌상단 좌표
                w = abs(self.start_pos.x() - self.end_pos.x()) # 드래그 시작점과 끝점의 X 좌표간의 차이
                h = abs(self.start_pos.y() - self.end_pos.y()) # W, H는 드래그된 마우스 포인터의 가로와 세로 길이
                screen = QApplication.primaryScreen()
                screenshot = screen.grabWindow(0, x, y, w, h) # window 인덱스? 몰라, x
                base_path = os.path.dirname("/home/rapa/.thumbnail")
                self.capture_folder_path = os.path.join(base_path, "capture")
                if not os.path.exists(self.capture_folder_path):
                        os.makedirs(self.capture_folder_path)
                screenshot_file_path = os.path.join(self.capture_folder_path, "screenshot.jpg")
                screenshot.save(screenshot_file_path, "jpg", quality=100)
                print(f"{screenshot_file_path}에 스크린샷이 저장되었습니다.")
                
                pixmap =QPixmap(screenshot_file_path)
                self.label_thum_img.setPixmap(pixmap)
                self.label_thum_img.setScaledContents(True)      
                QApplication.restoreOverrideCursor()
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PublishHandler()
    window.show()
    sys.exit(app.exec())

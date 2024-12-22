import os, sys, nuke, datetime, subprocess, re ,json

sys.path.append("/usr/local/lib/python3.6/site-packages")
# sys.path.append("/home/rapa/_phoenix_/Launcher/Loader/LoaderSceneSettingNuke")########################################원진추가###########################################################################
from shotgun_api3 import Shotgun
from Launcher.Loader.LoaderSceneSettingNuke.nk_validator_advanced import NukeValidator#######################################원진추가#############################################
try:
    from PySide6.QtWidgets import *
    from PySide6.QtUiTools import *
    from PySide6.QtCore import *
    from PySide6.QtGui import *
except ImportError:
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *

class PublishHandler(QMainWindow):
    USER_HOME_ROOT_PATH = '/home/rapa'
    def __init__(self):
        super().__init__()
        self.node_widgets = {}  # 노드 이름과 QTreeWidgetItem을 연결하는 딕셔너리
        self.connect_shotgrid()
        self.setting()
        self.first_show()
        self.update_file_info()
        self.center()
        
        QTimer.singleShot(0, self.make_screenshot)
        self.ui.pushButton_publish.clicked.connect(self.start_publish)
        self.ui.pushButton_validate.clicked.connect(self.start_validate)
    
    def start_validate(self):########################################################################################################################원진추가###########################################################################
        """validation 버튼 클릭시 호출되는 함수입니다."""
        self.ui.plainTextEdit_validation_report.clear()
        report = self.nuke_validator.get_script_validation_result()
        self.ui.plainTextEdit_validation_report.setPlainText(report)
    
    def start_publish(self):########################################################################################################################원진추가###########################################################################
        """publsih 버튼 클릭시 호출되는 함수입니다."""
        self.start_validate()
        self.export_selected_nodes()
        
        
    def connect_shotgrid(self): 
        self.sg = Shotgun(
            "https://4thacademy.shotgrid.autodesk.com/",  
            script_name="yumi",              
            api_key="jrqfdkq6mage-brSpdwvazpyk"                   
        )
        
    def setting(self):
        ui_file_path = f"{PublishHandler.USER_HOME_ROOT_PATH}/_phoenix_/ui/publisher.ui"
        ui_file = QFile(ui_file_path)

        self.ui = QUiLoader().load(ui_file, self)
        self.label_thum_img = self.ui.findChild(QLabel,"label_thum_img")
        self.nuke_validator = NukeValidator()########################################################################################################################원진추가###########################################################################
        # Screen_Capture 객체 생성 시 parent로 self.ui를 설정
        self.capture = ScreenCapture(self.label_thum_img, parent=self.ui)
        ui_file.close()
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
    def center(self):   # 창 가운데 띄우기
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        new_top_left = qr.topLeft()
        self.move(new_top_left)
        
    def closeEvent(self, event):
        # UI창이 닫힐 때 호출되는 메서드
        if hasattr(self, 'capture') and self.capture:
            self.capture.close()  # Screen_Capture 객체 종료
        QApplication.restoreOverrideCursor()  # 커서 상태 복원
        self.label_thum_img.clear()
        event.accept()  # 창 닫기 이벤트를 받아들임
        
    def first_show(self):
        user_id = self.get_user_id()
        project_id = self.get_project_id()
        
        self.ui.label_username.setText(self.get_user_name(user_id))
        self.ui.label_project_name.setText(self.get_project_name(project_id))
        self.tree_widget = self.ui.findChild(QTreeWidget, "treeWidget_main")
        self.label_file_name = self.ui.findChild(QLabel, "label_file_name")
        self.label_file_name2 = self.ui.findChild(QLabel, "label_file_name2")
        self.label_icon = self.ui.findChild(QLabel, "label_icon")
        self.label_file_type = self.ui.findChild(QLabel, "label_file_type")
        self.label_file_name_context = self.ui.findChild(QLabel, "label_file_name_context")
        self.description = self.ui.findChild(QTextEdit, "description")

        self.get_project_root()

        if self.tree_widget.topLevelItemCount() > 0:
            first_item = self.tree_widget.topLevelItem(0)
            self.tree_widget.setCurrentItem(first_item)
            self.get_file_info(first_item, 0)
        
        self.tree_widget.itemClicked.connect(self.get_file_info)

    def update_file_info(self):

        self.ui.label_summary_context.setText("render output for compositing.")
        self.frame_rate = int(nuke.root().knob('fps').value())
        self.start_frame = int(nuke.root().knob('first_frame').value())
        self.last_frame = int(nuke.root().knob('last_frame').value())
        
        # UI에 표시할 file_info 업데이트
        file_info = (
            f"Frame Rate: {self.frame_rate}\n"
            
            f"Frame Range: {self.start_frame} - {self.last_frame}"
        )
        self.label_file_name_context.setText(file_info)
        
    def make_screenshot(self):
        self.capture = ScreenCapture(self.label_thum_img)
        self.capture.show()

    def get_project_id(self):   # 프로젝트 데이터 가져오기 
        json_path = '/home/rapa/_phoenix_/Launcher/Loader/data_from_loader/json_from_loader.json'
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        # 254
        project_id = json_data['project_id']
        return project_id    
    
    def get_user_id(self):   # 유저 정보 가져오기
        json_path = '/home/rapa/_phoenix_/Launcher/Loader/data_from_loader/json_from_loader.json'
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        # 90
        user_id = json_data['user_id']
        return user_id
    
    def get_user_name(self, user_id):
        users = self.sg.find_one('HumanUser', [['id', 'is', user_id]], ['name'])
        if users:  # 결과가 존재하는지 확인
            return users['name']
        return "Unknown User"
    
    def get_project_name(self, project_id): 
        projects = self.sg.find_one('Project', [['id', 'is', project_id]], ['name'])
        if projects:  # 결과가 존재하는지 확인
            return projects['name']
        return "Unknown Project"

    def get_local_path(self, absolute_path):
        return os.path.normpath(absolute_path)
        
    def get_project_root(self):
        if nuke.root().name():
            self.nuke_path = nuke.root().name()  # Nuke의 경우 현재 스크립트 파일의 경로를 가져옴
            project_root = os.path.dirname(self.nuke_path)
            self.load_file(self.nuke_path)
    
    def load_file(self, *file_paths):
        for file_path in file_paths:
            if os.path.exists(file_path) and file_path.endswith(('.nknc', '.nk')):
                file_name = os.path.basename(file_path)
                # parent_item 생성
                parent_item = QTreeWidgetItem(self.tree_widget)
                parent_item.setText(0, file_name)
                parent_item.setToolTip(0, file_path)
                
                # 각 파일에 대해 nuke_submitter를 호출하여 sub_item 추가
                self.nuke_submitter(parent_item)

    def get_file_info(self, item, column):
        # 파일 정보 업데이트 호출
        self.update_file_info()
        
        # sub_item의 정보는 parent_item의 정보를 따른다.
        if item.parent() is not None:
            item = item.parent()
            
        selected_file_name = item.text(column)
        self.label_file_name.setText(selected_file_name)
        self.label_file_name2.setText(selected_file_name)

        
        file_extension = os.path.splitext(selected_file_name)[-1].lower()
        if file_extension in ['.nk', '.nknc']:
            pixmap = QPixmap(f"{PublishHandler.USER_HOME_ROOT_PATH}/_phoenix_/ui/image_source/Nuke.png")
            file_type = "Nuke Session"
        else:
            pixmap = QPixmap()
            file_type = "Unknown File Type"
        
        self.label_icon.setPixmap(pixmap)
        self.label_icon.setScaledContents(True)
        self.label_file_type.setText(file_type)

    def sync_checkboxes(self, state, checkboxes):
        for checkbox in checkboxes:
            checkbox.setCheckState(Qt.CheckState(state))
    
    def nuke_submitter(self, parent_item):
        node_list = []
        nodes = nuke.allNodes()  
        
        # Write 및 WriteGeo 노드만 node_list에 추가
        for node in nodes:
            if node.Class() in ["Write", "WriteGeo"]:
                node_list.append(node)
        
        def get_node_name(node):
            return node.name()
        
        sorted_nodes = sorted(node_list, key=get_node_name)
        
        for node in sorted_nodes:
            item_widget = QWidget()
            layout = QHBoxLayout(item_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            
            label = QLabel(f"{node.name()} ({node.Class()})")
            
            checkbox = QCheckBox()
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

            layout.addWidget(label)
            layout.addItem(spacer)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignLeft)
            layout.setContentsMargins(0, 0, 20, 0)
            
            # sub_item 생성
            sub_item = QTreeWidgetItem(parent_item)
            parent_item.addChild(sub_item)
            self.ui.treeWidget_main.setItemWidget(sub_item, 0, item_widget)
            
            # sub-item 열린상태로 시작 
            parent_item.setExpanded(True)
            sub_item.setExpanded(True)
            
            self.node_widgets[node.name()] = sub_item
            
    def export_selected_nodes(self):
        # 선택된 노드 이름을 필터링하여 가져옴
        selected_nodes = []
        for node_name, tree_item in self.node_widgets.items():
            # 트리 항목에서 widget을 가져오고 그 안의 체크박스를 찾음
            item_widget = self.ui.treeWidget_main.itemWidget(tree_item, 0)
            if item_widget:
                checkbox = item_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    selected_nodes.append(node_name)

        if not selected_nodes:
            print("노드가 선택되지 않았습니다.")
            return
        
        file_path = nuke.scriptName()
        created_version,created_published_file,new_version_code = self.shotgrid_setting(file_path)
        
        # 선택된 각 노드에 대해 export 함수 호출
        for node_name in selected_nodes:
            self.export(node_name,new_version_code,created_version,created_published_file)
            
    def shotgrid_setting(self, file_path): # create link
        
        #local_file_path 설정
        if self.nuke_path:
            local_file_path =self.get_local_path(self.nuke_path)
        else:
            QMessageBox.critical(self, "업로드 실패", "Nuke path가 지정되지 않았습니다.")
            return
        
        file_path =local_file_path      
        
        print(f"file_path: {file_path}")
        
        # naming : Sequence_Shot_task_wip_v001.nknc
        user_id = self.get_user_id()  ## 로그인 정보 가져와서 바꿔주기..
        project_id = self.get_project_id()
        file_name = os.path.basename(file_path)  # Sequence_Shot_task_wip_v001.nknc
        self_file_base_name = file_name.split('.')[0] # Sequence_Shot_task_wip
        shot_name = '_'.join(self_file_base_name.split('_')[:2]) # Sequence_Shot
        task_name='_'.join(self_file_base_name.split('_')[:3]) # Sequence_Shot_task
        sequence_name = self_file_base_name.split('_')[0] #Sequence
        ver_name= '_'.join(self_file_base_name.split('_')[:4])
        
        try: 
            # 시퀀스 유무 확인 , 없으면 생성 
            sequence_data = self.sg.find_one("Sequence",[['project','is',{'type': 'Project', 'id': project_id}], ['code', 'is', sequence_name]])
            if sequence_data:
                sequence_id = sequence_data['id']
                print(f"{sequence_name} 시퀀스가 이미 존재 합니다. ID:{sequence_id}")

            else: 
                sequence_data = {
                    'project': {'type': 'Project', 'id': project_id},
                    'code': sequence_name,
                    'description': f'{sequence_name} 시퀀스 입니다',
                    'sg_status_list': 'ip'
                }
                created_sequence = self.sg.create('Sequence', sequence_data)
                sequence_id = created_sequence['id']
                print(f"{sequence_name} 시퀀스가 생성되었습니다")


            # Shot 유무 확인, 없으면 생성
            shot_data = self.sg.find_one("Shot",[['project','is',{'type':'Project','id':project_id}],['code','is',shot_name]])
            if shot_data:
                shot_id = shot_data["id"]
                print(f"{shot_name} 샷이 이미 존재합니다. ID: {shot_id}")

            else:
                shot_data = {
                    'project': {'type': 'Project', 'id': project_id},
                    'code': shot_name,
                    'sg_sequence': {'type': 'Sequence', 'id': sequence_id},
                    'description': f'{shot_name} 샷 입니다',
                    'sg_status_list': 'pub'
                }
                created_shot = self.sg.create('Shot', shot_data)
                shot_id = created_shot['id']
                print(f"{shot_name} 샷이 생성되었습니다.")

            # Task 유무 확인, 없으면 생성
            task_data = self.sg.find_one('Task', [['project', 'is', {'type': 'Project', 'id': project_id}], ['entity', 'is', {'type': 'Shot', 'id': shot_id}], ['content', 'is', task_name]])
            if task_data:
                task_id = task_data["id"]
                print(f"{task_name} Task가 이미 존재합니다. ID: {task_id}")
            else: 
                created_task = self.sg.create("Task", {
                    "project": {"type": "Project", "id": project_id},
                    "entity": {"type": "Shot", "id": shot_id},
                    "content": task_name,
                    'step': {'type': 'Step', 'id': 8}, #  comp로 지정
                    "task_assignees": [{"type": "HumanUser", "id": user_id}], 
                    "sg_status_list": "pub",
                })
                task_id = created_task['id']
                print(f"{created_task['id']} Task가 생성되었습니다.")

            #UI에 입력된 description
            description = self.description.toPlainText().strip()
            
            # Version 없으면 v001으로, 있으면 버젼업
            version_data = self.sg.find('Version',[
                    ['project', 'is', {'type': 'Project', 'id': project_id}], 
                    ['entity', 'is', {'type': 'Shot', 'id': shot_id}], 
                    ['code', 'starts_with', '_'.join(self_file_base_name.split('_')[:-2])]], ['code','sg_status_list'])
            
            print('_'.join(self_file_base_name.split('_')[:-1]))
            print(f"version_data: {version_data}")
            
            if version_data:
                # Version이 이미 존재하면 새로운 버전을 만듬.
                # 가장 큰 버전 번호를 찾음
                
                latest_version_code = None
                max_version_number = 0
                for version in version_data:
                    if version['sg_status_list'] =='pub':
                        current_code = version['code'] # 버전 번호를 추출 (예: _v001에서 1을 추출)
                        match = re.search(r'_v(\d+)$', current_code)
                        if match:
                            version_number = int(match.group(1))
                            if version_number > max_version_number:
                                max_version_number = version_number
                                latest_version_code = current_code
                print(f"마지막 버젼 코드: {latest_version_code}")       
                
                out_ver = '_'.join(latest_version_code.split('_')[:-1])
                new_version_number = max_version_number + 1
                new_version_code = f"{out_ver}_v{str(new_version_number).zfill(3)}"  # 버전 번호 증가
                print(f"새로운 버젼 코드: {new_version_code}")
                    
            else:
                new_version_code = f"{ver_name.replace('wip','pub')}_v001"
                
            file_type = self.sg.find_one("PublishedFileType", [["code", "is", "Nuke Script"]], ["id"])
                    
            created_version = self.sg.create("Version", {
                "project": {"type": "Project", "id": project_id},
                "code": new_version_code,
                "sg_path": local_file_path,
                "sg_version_file_type":{"type": "PublishedFileType", "id": file_type["id"]},
                "sg_status_list": "pub",  
                "entity": {"type": "Shot", "id": shot_id},
                "sg_task": {"type": "Task", "id": task_id},
                "user": {"type": "HumanUser", "id": user_id},
                "description": description         #UI에 입력된 description 사용
            })
            print(f"{new_version_code} 버젼을 업로드했습니다.")
            
            
            created_published_file = self.sg.create("PublishedFile",{
                "project": {"type": "Project", "id": project_id},
                "entity": {"type": "Shot", "id": shot_id},
                "task": {"type": "Task", "id": task_id},
                "code": new_version_code,
                "path": {"local_path": local_file_path}, 
                "published_file_type": {"type": "PublishedFileType", "id": file_type["id"]},
                "description": description         #UI에 입력된 description 사용 
                })
            print(f"{new_version_code} 퍼블리쉬 파일을 업로드 했습니다.")
            
            return created_version, created_published_file ,new_version_code
                    
        except KeyError as e:
            print(f"KeyError occurred: {e}") 

    def export(self,node_name, new_version_code, created_version, created_published_file):
        file_path = nuke.scriptName()
        split = file_path.split(".")                
        
        # 설정된 first_frame과 last_frame을 가져옴
        first_frame = int(nuke.root().knob('first_frame').value())
        last_frame = int(nuke.root().knob('last_frame').value())

        #폴더 경로 생성
        base_path = os.path.dirname(file_path)
        print("base_path는"f"{base_path}입니다,")

        ver = new_version_code.split("_")[-1]
                
        self.ver_folder_path =os.path.join(base_path,ver)
        self.exr_folder_path =os.path.join(self.ver_folder_path, "exr")
        self.mov_folder_path =os.path.join(self.ver_folder_path, "mov")
        self.exr_nodename_folder_path = os.path.join(self.exr_folder_path, node_name)
        self.mov_nodename_folder_path =os.path.join(self.mov_folder_path,node_name)
        
        print("folder_path는"f"{self.ver_folder_path}입니다.")
        print("exr folder_path는"f"{self.exr_folder_path}입니다")
        print("mov folder_path는"f"{self.mov_folder_path}입니다.")
        
        #폴더가 존재하지 않으면 생성
        if not os.path.exists(self.ver_folder_path):
            os.makedirs(self.ver_folder_path)
        
        if not os.path.exists(self.exr_folder_path):
            os.makedirs(self.exr_folder_path)
            
        if not os.path.exists(self.mov_folder_path):
            os.makedirs(self.mov_folder_path)
            
        if not os.path.exists(self.exr_nodename_folder_path):
            os.makedirs(self.exr_nodename_folder_path)
            
        if not os.path.exists(self.mov_nodename_folder_path):
            os.makedirs(self.mov_nodename_folder_path)
        
        self.exr_path = os.path.join(self.exr_nodename_folder_path, f"{new_version_code.replace('wip','pub')}_{node_name}.####.exr")
        print("exr_path는"f"{self.exr_path}입니다.")

        self.mov_path = os.path.join(self.mov_nodename_folder_path, f"{new_version_code.replace('wip','pub')}_{node_name}.mov")
        print("mov_path는" f"{self.mov_path}입니다.")
        
        node = nuke.toNode(node_name)
        
        if not node:
            print(f"Node {node_name} not found.")
            return
        
        node.knob("file").setValue(self.exr_path)
        node.knob("file_type").setValue("exr")                                                                                                                                                                                                                                                                                                                                                                       
        nuke.execute(node_name,first_frame,last_frame)
        print(f"{node_name}: EXR render 완료되었습니다.")
    
        node.knob("file").setValue(self.mov_path)
        node.knob('file_type').setValue("mov")
        nuke.execute(node_name)
        print(f"{node_name}: MOV render 완료되었습니다.")
        
        # 속성 업데이트 후 파일 정보 갱신
        self.frame_rate = int(nuke.root().knob("fps").value())
        self.start_frame = first_frame
        self.last_frame = last_frame
        
        # export가 끝나면 슬레이트 만들기
        project_id = self.get_project_id()
        self.encode_video(node_name, project_id, created_version, created_published_file, new_version_code)

    def encode_video(self,node_name,project_id,created_version, created_published_file, new_version_code):
        
        node = nuke.toNode(node_name)
        root = nuke.root()
        input_node = node.input(0)  # Write 노드에 연결된 입력 노드를 가져옴
        image_path = self.mov_path # export에서 내보낸 mov 경로  
        ###################################################################

        #file name info 
        file_path = nuke.scriptName()
        file_name = os.path.basename(file_path)  # Sequence_Shot_task_v001.nknc
        self.file_base_name = file_name.split('.')[0] # Sequence_Shot_task_v001
        self.shot_name = '_'.join(self.file_base_name.split('_')[:2]) # Sequence_Shot
        
        #######################################################################
        self.start_frame = int(root.knob("first_frame").value())
        self.last_frame = int(root.knob("last_frame").value())
        self.frame_rate = int(root.knob("fps").value())
        first = self.start_frame 
        frame_count = self.last_frame - self.start_frame  
        
        self.slate_size = 60
        self.font_size = 40
        self.text_x_padding = 10
        self.text_y_padding = 20
        self.font_path = f"{PublishHandler.USER_HOME_ROOT_PATH}/_phoenix_/ui/font/Courier_Regular/Courier_Regular.ttf"
        ###################################################################
        
        if input_node:
            width = input_node.width()    # 입력 노드의 너비를 가져옴
            height = input_node.height()  # 입력 노드의 높이를 가져옴
        
        #################################################################       
        top_left = f"{self.shot_name}"
        top_center = self.get_project_name(project_id)
        top_right = datetime.date.today().strftime("%Y/%m/%d")
        bot_left = f"{width}x{height}"
        bot_center = ""
        
        frame_cmd = "'Frame \\: %{eif\\:n+"
        frame_cmd += "%s\\:d}' (%s)"  % (first, frame_count+1)
        bot_right = frame_cmd

        self.slate_path = os.path.join(self.mov_nodename_folder_path, f"{new_version_code.replace('wip','pub')}_{node_name}_slate.mov")
        print("slate_path는"f"{self.slate_path}")
        
        ################################################################   

        cmd = (
                f'ffmpeg -r {self.frame_rate} -y -i {image_path} '
                f'-vf "drawbox=y=0:color=black:width=iw:height={self.slate_size}:t=fill,'
                f'drawbox=y=ih-{self.slate_size}:color=black:width=iw:height={self.slate_size}:t=fill,'
                f'drawtext=fontfile={self.font_path}:fontsize={self.font_size}:fontcolor=white@0.7:text={top_left}:x={self.text_x_padding}:y={self.text_y_padding},'
                f'drawtext=fontfile={self.font_path}:fontsize={self.font_size}:fontcolor=white@0.7:text={top_center}:x=(w-text_w)/2:y={self.text_y_padding},'
                f'drawtext=fontfile={self.font_path}:fontsize={self.font_size}:fontcolor=white@0.7:text={top_right}:x=w-tw-{self.text_x_padding}:y={self.text_y_padding},'
                f'drawtext=fontfile={self.font_path}:fontsize={self.font_size}:fontcolor=white@0.7:text={bot_left}:x={self.text_x_padding}:y=h-th-{self.text_y_padding},'
                f'drawtext=fontfile={self.font_path}:fontsize={self.font_size}:fontcolor=white@0.7:text={bot_center}:x=(w-text_w)/2:y=h-th-{self.text_y_padding},'
                f'drawtext=fontfile={self.font_path}:fontsize={self.font_size}:fontcolor=white@0.7:text={bot_right}:x=w-tw-{self.text_x_padding}:y=h-th-{self.text_y_padding}" '
                f'-c:v prores_ks -profile:v 3 -colorspace bt709 {self.slate_path}'
            )
        subprocess.run(cmd, shell=True)
        
        print("슬레이트를 만들었습니다.")
        self.upload_to_shotgrid(created_version, created_published_file)

    def upload_to_shotgrid(self, created_version,created_published_file):
        try:
             # version에 슬레이트 업로드 
             version_id = created_version['id']
             new_version_code = created_version['code']
             self.sg.upload("Version", version_id, self.slate_path, field_name="sg_uploaded_movie")
             print(f"{new_version_code} 슬레이트가 업로드되었습니다.")

             published_id = created_published_file['id']
             if hasattr(self, 'capture') and self.capture:
                 screenshot_file_path = os.path.join(self.capture.capture_folder_path, "screenshot.jpg")
                 if os.path.exists(screenshot_file_path):
                     self.sg.upload_thumbnail("PublishedFile", published_id, screenshot_file_path)

             self.sg.update("PublishedFile", int(published_id), {"sg_exr_path": self.exr_folder_path})
             print("exr 파일이 업로드 되었습니다.")

             # 생성된 PublishedFile을 기존 Version에 추가
             link_publish_version = self.sg.update("Version", version_id,
                                                   {"published_files": [{"type": "PublishedFile", "id": published_id}]})
             print(f"Version ID {version_id}에 Publish Version ID {link_publish_version['id']}가 링크 되었습니다.")
             QMessageBox.information(self, "Upload Successful", f"'{new_version_code}' 버젼으로 퍼블리쉬 되었습니다.")
             
        except Exception as e:
            QMessageBox.critical(self, "업로드 실패", f"슬레이트와 썸네일 업로드에 실패하였습니다. Error: {str(e)}")


class ScreenCapture(QWidget):

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

   def paintEvent(self, event):
       """
       마우스가 드래그되는 곳에 사각형 그려주는 페인트 메서드
       """
       if self.start_pos and self.end_pos:
           rect = QRect(self.start_pos, self.end_pos)
           painter = QPainter(self)
           painter.setPen(Qt.white)
           painter.drawRect(rect)

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
           
           file_path = nuke.scriptName()
           base_path = os.path.dirname(file_path)
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

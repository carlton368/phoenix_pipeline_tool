

from Publisher.Maya.data_explorer_sj import DataExplorer
from Publisher.Maya.maya_pub_data_manager import MayaFileSaver
from typing import dict, str
class UploadDataToShotGrid(DataExplorer):
    
    def __init__(self,project_name,task_step) -> None:
        super(DataExplorer).__init__()
        publish_file_type = self.get_file_type()
        self.file_saver = MayaFileSaver()

    def get_file_type(self):
        published_file_type = self.sg.find_one("PublishedFileType", [["code", "is", "Maya Scene"]], ["id"])
        
        return published_file_type
    
    def upload_to_shotgrid(self,
                           pub_path : str,
                           project_name : str, 
                           entity : dict, 
                           code, 
                           ma_path, 
                           json_path):
        
        if self.task_step == "lkd":
            maya_slate_path = self.file_saver.asset_make_slate(self.pub_path, self.get_project_name())
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 254},
            'sg_path': self.ma_path, #이게 두번 올라감..?
            'sg_status_list': 'pub', #user 정보 올라가야함
            'sg_shader_json_path': f"{self.json_path}",
            'sg_version_file_type': published_file_type
            })
            published_file_type = self.sg.find_one("PublishedFileType", [["code", "is", "Maya Scene"]], ["id"])
            if not published_file_type:
                print("'Maya Scene'이 없습니다.")
                return
            created_published_file = self.sg.create("PublishedFile",{
                "project": {"type": "Project", "id": 254},
                "entity": entity,
                "task": {"type": "Task", "id": task_id}, 
                "path": {"local_path": self.ma_path}, 
                "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사용
                'path_cache':self.json_path,
                'sg_status_list':'ip',
                'published_file_type': published_file_type
            })
                    

                
        #리깅일 경우.. mb 파일로만 나감
        elif self.task_step == "rig":
            maya_slate_path = self.file_saver.asset_make_slate(self.pub_path, self.get_project_name())
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 254},
            'sg_path': self.pub_path,
            'sg_status_list': 'pub', #user 정보 올라가야함,
            'sg_version_file_type': published_file_type
            
                
            })
            
            created_published_file = self.sg.create("PublishedFile",{
                    "project": {"type": "Project", "id": 254},
                    "entity": entity,
                    "task": {"type": "Task", "id": task_id}, 
                    "path": {"local_path": self.pub_path}, 
                    "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사
                    'published_file_type': published_file_type
            })   
            
        elif self.task_step == "mod":
            maya_slate_path = self.file_saver.asset_make_slate(self.pub_path, self.get_project_name())
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 254},
            'sg_path': self.mb_path,
            'sg_status_list': 'pub', #user 정보 올라가야함   
            'sg_cache_path':f"{self.cache_path}",
            'sg_version_file_type': published_file_type
            
        })
            created_published_file = self.sg.create("PublishedFile",{
                "project": {"type": "Project", "id": 254},
                "entity": entity,
                "task": {"type": "Task", "id": task_id}, 
                "path": {"local_path": self.mb_path }, 
                "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사용
                'path_cache':f"{self.cache_path}",
                'published_file_type': published_file_type
            })
            #lighting은 exr 렌더 후, 이미지의 경로 + 
            #mb,cache 나가야함.
            
        elif self.task_step == "lgt":
            
            created_published_file = self.sg.create("PublishedFile",{
                    "project": {"type": "Project", "id": 254},
                    "entity": entity,
                    "task": {"type": "Task", "id": task_id}, 
                    "path": {"local_path": self.pub_path}, 
                    "description": self.ui.description.toPlainText(),   #UI에 입력된 desmaya_slate_pathcription 사
                    'published_file_type': published_file_type
            })   
            return created_published_file
            
        elif self.task_step == "ani": # 만약에 anim_cam 이 있다면, 카메라 캐쉬 나가주게 짜야함,
            maya_slate_path = self.file_saver.shot_make_slate(self.pub_path, self.get_project_name())
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 254},
            'sg_path': self.pub_path,
            'sg_status_list': 'pub', #user 정보 올라가야함   
            'sg_cache_path':f"{self.cache_path}",
            'sg_version_file_type': published_file_type
            
        })
            created_published_file = self.sg.create("PublishedFile",{
                "project": {"type": "Project", "id": 254},
                "entity": entity,
                "task": {"type": "Task", "id": task_id}, 
                "path": {"local_path": self.pub_path }, 
                "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사용
                'path_cache':f"{self.cache_path}",
                'published_file_type': published_file_type
            })
            
        elif self.task_step == "mm": #카메라 캐쉬 나가줘야하나?
            maya_slate_path = self.file_saver.shot_make_slate(self.pub_path, self.get_project_name())
            width, height = self.infocatcher.get_render_resolution()
            new_version = self.sg.create('Version', {
            'entity': entity,
            'sg_task': {'type': 'Task', 'id': task_id},
            'code': f'{code}',
            'description':  self.ui.description.toPlainText() , ###########고쳐야함
            'project': {'type': 'Project', 'id': 254},
            'sg_path': self.pub_path,
            'sg_status_list': 'pub', #user 정보 올라가야함   
            'sg_cache_path':f"{self.cache_path}",
            'sg_version_file_type': published_file_type,
            
        })
            created_published_file = self.sg.create("PublishedFile",{
                "project": {"type": "Project", "id": 254},
                "entity": entity,
                "task": {"type": "Task", "id": task_id}, 
                "path": {"local_path": self.pub_path }, 
                "description": self.ui.description.toPlainText(),   #UI에 입력된 description 사용
                'path_cache':f"{self.cache_path}",
                'published_file_type': published_file_type
                
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
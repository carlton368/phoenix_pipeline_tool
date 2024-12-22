from shotgun_api3 import Shotgun
import os

class FileSaver():
    def __init__(self):
        self.sg = Shotgun(
            "https://4thacademy.shotgrid.autodesk.com",
            "kangseyoung",
            "imthtqts8zqqXylfckoiihx-z"
        )
        
    def save_in_local(self, file_type, file_path):
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # 열린 파일이 누크일 때 로컬에 저장
        if file_type == 'Nuke':
            import nuke
            nuke.scriptSaveAs(file_path)
            print('파일이 저장되었습니다.')
            print(f'file path : {file_path}')
        
        elif file_type == "Maya":
            import maya.cmds as cmds
            cmds.file(rename=file_path)
            # cmds.file(save=True, type='mayaAscii')
            cmds.file(save=True, type='mayaBinary')
            print('파일이 저장되었습니다.')
            print(f'file path : {file_path}')
    
    def upload_to_shotgrid(self, save_info, entity_type,file_path, ext, user_id ):
        print("샷그리드 업로드 시작")
        print(f"save_info : {save_info}")
        print(f"entity_type : {entity_type}")
        print(f"file_path : {file_path}")
        file_name = file_path.split('/')[-1]
        ver_name = file_name.split('.')[0]
        project_id = save_info['project']['id']
        
        if entity_type == "Shots":
            shot_id = save_info['shot']['id']
            task_id = save_info['task']['id']
            
            if ext in ['nk', 'nknc']:
                file_type_id = 1
            elif ext in ['ma', 'mb']:
                file_type_id = 67
            
            created_version = self.sg.create("Version", {
                "project": {"type": "Project", "id": project_id},
                "code": ver_name,
                "sg_path":file_path,
                "sg_status_list": "wip",  
                "entity": {"type": "Shot", "id": shot_id},
                "sg_task": {"type": "Task", "id": task_id},
                "sg_version_file_type" : {'type': 'PublishedFileType', 'id': file_type_id},
                "user": {"type": "HumanUser", "id": user_id}
            })
            print(f"{created_version['id']} 버젼이 생성되었습니다.")
            
        elif entity_type == "Assets":
            print("샷그리드 업로드 시작")
            print(f"save_info : {save_info}")
            print(f"entity_type : {entity_type}")
            print(f"file_path : {file_path}")
            asset_type = save_info['asset_type']
            asset_id = save_info['asset']['id']
            task_id = save_info['task']['id']
            
            if ext in ['nk', 'nknc']:
                file_type_id = 1
            elif ext in ['ma', 'mb']:
                file_type_id = 67
            
            created_version = self.sg.create("Version", {
                "project": {"type": "Project", "id": project_id},
                "code": ver_name,
                "sg_path":file_path,
                "sg_status_list": "wip",  
                "entity": {"type": "Asset", "id": asset_id},
                "sg_task": {"type": "Task", "id": task_id},
                "sg_version_file_type" : {'type': 'PublishedFileType', 'id': file_type_id},
                "user": {"type": "HumanUser", "id": user_id}
            })
            print(f"{created_version['id']} 버젼이 생성되었습니다.")
        
        return created_version['id']


from typing import List, Dict, Any
from pprint import pprint
import os
import sys
import shutil
import sys
import shotgun_api3
import requests

class DataExplorer:
    def __init__(self):
        self.sg = shotgun_api3.Shotgun(
            "https://4thacademy.shotgrid.autodesk.com",
            "kangseyoung",
            "imthtqts8zqqXylfckoiihx-z"
        )
        
    def get_user_name(self,user_id: int): #######################
        """
        지정된 유저의 이름을 가져옵니다
        """
        users =  self.sg.find_one('HumanUser', [['id', 'is', user_id]], ['name'])
        user_name = users['name']
        return user_name
    
    def get_assigned_works(self,user_id: int) -> List[Dict[str, Any]]:#######################
        """
        user_id 를 인풋으로 받고, 할당된 task들을 리턴.
        """
        filters = [
                ['task_assignees', 'is', {'type': 'HumanUser', 'id': user_id}]
            ]
            
            # 가져올 필드 목록 설정 (원하는 필드를 추가할 수 있음)
        fields = ['step', 'due_date', 'entity', 'sg_status_list']

            # 테스크 검색
        tasks = self.sg.find('Task', filters, fields)
        
        total_dic = {}
        for task in tasks:
            if task['entity']['type'] == 'Shot':
                shot_name = task['entity']['name']
                shot_id = task['entity']['id']
                seq_list = self.sg.find_one('Shot',[['id', 'is', shot_id]], ['sg_sequence'])
                for seq_info in seq_list:
                    seq_name = seq_info['sg_sequence']['code']
                    seq_id = seq_info['sg_sequence']['id']
                    total_dic.append({'shot' : {'id': shot_id,'name' : shot_name}, 
                                      'sequence' : {'id' : seq_id, 'name' : seq_name}})
                
            
                
        
        return tasks

    def get_projects(self) -> List[Dict[str, Any]]:
        """프로젝트 목록을 가져옵니다."""
        return self.sg.find("Project", [], ["name", "id", "sg_status"])
    
    def get_project_name(self,project_id: int):#######################
        """프로젝트 이름을 가져옵니다."""
        projects =  self.sg.find_one('Project', [['id', 'is', project_id]], ['name'])
        project_name = projects['name']
        return project_name
    
    def get_asset_types(self,project_id: int) -> List[Dict[str, Any]]:#######################
        """지정된 프로젝트의 에셋 타입 목록을 가져옵니다."""
        assets = self.sg.find("Asset", [['project', 'is', {'type': 'Project', 'id': project_id}]], 
                            ["sg_asset_type"])
        asset_type_list = []
        for asset in assets:
            if not asset['sg_asset_type'] in asset_type_list:
                asset_type_list.append(asset['sg_asset_type'])
            
        return asset_type_list

    def get_assets(self, project_id: int) -> List[Dict[str, Any]]:
        """지정된 프로젝트의 에셋 목록을 가져옵니다."""
        return self.sg.find("Asset", [['project', 'is', {'type': 'Project', 'id': project_id}]], 
                            ["code", "id", "sg_asset_type"])
        
    def get_sequences(self, project_id: int) -> List[Dict[str, Any]]:
        """지정된 프로젝트의 시퀀스 목록을 가져옵니다."""
        return self.sg.find("Sequence", [['project', 'is', {'type': 'Project', 'id': project_id}]], 
                            ["code"])

    def get_shots(self, sequence_id: int) -> List[Dict[str, Any]]:
        """지정된 시퀀스의 샷 목록을 가져옵니다."""
        return self.sg.find("Shot", [['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}]], 
                            ["code", "name"])

    def get_shot_tasks(self, shot_id: int) -> List[Dict[str, Any]]:####
        """지정된 샷의 태스크 목록을 가져옵니다."""
        return self.sg.find("Task", [['entity', 'is', {'type': 'Shot', 'id': shot_id}]], 
                            ["content","step", "sg_status_list"])
        
    def get_asset_tasks(self, asset_id: int) -> List[Dict[str, Any]]:####
        """지정된 에셋의 태스크 목록을 가져옵니다.."""
        return self.sg.find("Task", [['entity', 'is', {'type': 'Asset', 'id': asset_id}]], 
                            ["content","step","sg_status_list"])
        
    def get_version(self, task_id: int) -> List[Dict[str, Any]]:##########################
        """지정된 태스크의 버젼목록을 가져옵니다."""
        
        versions = self.sg.find("Version", [['sg_task', 'is', {'type': 'Task', 'id': task_id}]], 
                            ["code", "sg_status_list", "created_at"])
        wip=[]
        pub=[]
        for version in versions:
            if version['sg_status_list'] == 'wip':
                
                wip.append(version['code'])
            if version['sg_status_list'] == 'pub':
                pub.append(version['code'])
        return wip, pub, versions
    
    def get_artist(self, version_id: int) -> str:    #####################################
        """지정된 버전 ID로 아티스트(사용자) 이름을 가져옵니다."""
        version_data = self.sg.find_one("Version", [['id', 'is', version_id]], 
                                        ["user"])  # 아티스트 정보가 포함된 필드
        
        if version_data and version_data.get("user"):
            artist_name = version_data["user"]["name"]
            return artist_name
        
    
    def download_thumbnail(self,task_id,save_path=None):
        """
        task_id를 받고, version별 썸네일 다운로드 받기..
        """
        if not save_path:
            save_path = '/home/rapa/thumbnail'
        path_list=[]
        
    
        # version = self.sg.find_one('Version', [['id', 'is', project_id]], ['image'])
        
        versions = self.sg.find("Version", [['sg_task', 'is', {'type': 'Task', 'id': task_id}]], 
                            ['image','sg_status_list','code'])
        
        for version in versions:
            path = save_path
            status = version['sg_status_list']
            version_id = version['id']
            version_code = version['code']
            if not version.get('image'):
                print(f"version {version['code']}에 대한 썸네일이 없습니다.")
                return None
            path +=f'/{status}'
            print(f"version {version['code']}에 대한 썸네일이 있습니다.{status}")
            thumbnail_url = version['image']
            if not thumbnail_url:
                print(f"version {version['code']}에 대한 썸네일 URL을 가져올 수 없습니다.")
                return None
            # 썸네일을 다운로드합니다.
            if not os.path.exists(f'{path}/version{version_id}_thumbnail.jpg') and not os.path.exists(path):    
                os.makedirs(path)
            with requests.get(thumbnail_url, stream=True) as response:
                response.raise_for_status()
                print('썸네일이 가져와짐')
                with open(f'{path}/version{version_code}_thumbnail.jpg', 'wb') as file:
                    shutil.copyfileobj(response.raw, file)
                    version_path={}
                    version_path[version_id]=f'{path}/version{version_code}_thumbnail.jpg'
                    path_list.append(version_path)
                    print(f"썸네일이 {path}/version{version_code}_thumbnail.jpg 에 저장되었습니다.")
        return path_list
    
        
        
        
    # def gt_status(self, status: str) -> List[Dict[str, Any]]:
    #     ""지정된 프로젝트의 작업 목록을 가져옵니다."""
    #     rturn self.sg.find("Task", [['entity', 'is', {'type': 'Shot', 'id': task_id}]], 
    #                        ["content", "sg_status_list"])    

    def get_entity_details(self, entity_type: str, entity_id: int) -> Dict[str, Any]:
        """특정 엔티티의 세부 정보를 가져옵니다."""
        return self.sg.find_one(entity_type, [["id", "is", entity_id]], ["*"])

if __name__ == "__main__":
    explorer = DataExplorer()
    
    user_tasks = explorer.get_assigned_works(98)
    print (user_tasks)
    
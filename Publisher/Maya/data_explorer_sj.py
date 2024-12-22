
from typing import List, Dict, Any
from pprint import pprint
import os
import sys
import shutil
import sys
import shotgun_api3
import requests

script_name = "kangseyoung"
script_key = "imthtqts8zqqXylfckoiihx-z"
#샷그리드에 데이터를 조회하는 모듈.

class DataExplorer:
    
    print("dataexplorer")
    
    def __init__(self):
        script_name = "kangseyoung"
        script_key = "imthtqts8zqqXylfckoiihx-z"
        
        self.sg = shotgun_api3.Shotgun(
            
            "https://4thacademy.shotgrid.autodesk.com",
            script_name = script_name,
            api_key = script_key
        )
    
    def get_user_name(self,user_id: int): #######################
        """
        지정된 유저의 이름을 가져옵니다
        """
        users =  self.sg.find_one('HumanUser', [['id', 'is', user_id]], ['name'])
        user_name = users['name']
        return user_name
    
    def get_assigned_works(self,user_id: int, project_id: int): #######################
        """
        user_id 를 인풋으로 받고, 할당된 task들을 리턴.
        """
        filters = [
                ['task_assignees', 'is', {'type': 'HumanUser', 'id': user_id}],
                ['project', 'is', {'type': 'Project', 'id': project_id}]
            ]
            
            # 가져올 필드 목록 설정 (원하는 필드를 추가할 수 있음)
        fields = ['step', 'due_date', 'entity', 'sg_status_list']

            # 테스크 검색
        tasks = self.sg.find('Task', filters, fields)
        # pprint(tasks)
        shot_list = []
        asset_list = []
        for task in tasks:
            if not task['sg_status_list'] in ['wip','wtg']:
                continue
            if not task['entity']:
                continue
            if task['entity']['type'] == 'Shot':
                task_name = task['step']['name']
                task_id = task['id']
                shot_name = task['entity']['name']
                shot_id = task['entity']['id']
                seq_dic = self.sg.find_one('Shot',[['id', 'is', shot_id]], ['sg_sequence'])
                seq_name = seq_dic['sg_sequence']['name']
                seq_id = seq_dic['sg_sequence']['id']
                shot_list.append({'task' : {'id': task_id ,"name": task_name},
                                  'shot' : {'id': shot_id,'name' : shot_name}, 
                                  'sequence' : {'id' : seq_id, 'name' : seq_name}})
            if task['entity']['type'] == 'Asset':
                task_name = task['step']['name']
                task_id = task['id']
                asset_name = task['entity']['name']
                asset_id = task['entity']['id']
                asset_dic = self.sg.find_one('Asset',[['id','is',asset_id]],['sg_asset_type'])
                asset_type = asset_dic['sg_asset_type']
                asset_list.append({'task' : {'id': task_id,"name": task_name},
                                   'asset_type' : asset_type,
                                   'asset' : {'id' : asset_id, 'name' : asset_name}})
        return tasks, shot_list, asset_list

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

    def get_shots(self, sequence_id: int):
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
    
    
    def download_thumbnail(self, task_id, save_path=None):
        if not save_path:
            save_path = '/home/rapa/thumbnail'
        path_list = []

        versions = self.sg.find("Version", [['sg_task', 'is', {'type': 'Task', 'id': task_id}]], 
                                ['image', 'sg_status_list', 'code'])
        # print(versions)

        for version in versions:
            path = save_path
            version_id = version['id']
            version_code = version['code']

            if not version.get('image'):
                print(f"version {version_code}에 대한 썸네일이 없습니다.")
                continue  # 다음 버전으로 건너뜀
            
            thumbnail_url = version['image']

            if not os.path.exists(path):    
                os.makedirs(path)

            try:
                with requests.get(thumbnail_url, stream=True) as response:
                    response.raise_for_status()
                    print('썸네일이 가져와짐')

                    file_path = f'{path}/version{version_code}_thumbnail.jpg'
                    with open(file_path, 'wb') as file:
                        shutil.copyfileobj(response.raw, file)
                        version_path = {version_id: file_path}
                        path_list.append(version_path)
                        print(f"썸네일이 {file_path}에 저장되었습니다.")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download thumbnail for version {version_code}: {e}")
                continue  # 현재 버전은 건너뛰고 다음 버전으로 이동
            
        if not path_list:
            print(f"No thumbnails found for task_id {task_id}.")

        return path_list
    
        
    # def gt_status(self, status: str) -> List[Dict[str, Any]]:
    #     ""지정된 프로젝트의 작업 목록을 가져옵니다."""
    #     rturn self.sg.find("Task", [['entity', 'is', {'type': 'Shot', 'id': task_id}]], 
    #                        ["content", "sg_status_list"])    

    def get_entity_details(self, entity_type: str, entity_id: int) -> Dict[str, Any]:
    
        """특정 엔티티의 세부 정보를 가져옵니다."""
        return self.sg.find_one(entity_type, [["id", "is", entity_id]], ["*"])


    def get_pub_version_code(self, sg_task): #세영 추가함
        try:
        # Connect to ShotGrid
            # Define the filter to find versions associated with the task
            filters = [['sg_task', 'is', sg_task]]
            fields = ['code', 'sg_path', 'description', 'project', 'sg_task', 'entity', 'sg_status_list']
            
            # Query ShotGrid to get versions for the specified task
            print ("hello ")
            versions = self.sg.find('Version', filters, fields)
            pub_version_list = []
            for version in versions:
                print ("version")
                print (version)
                if version['sg_status_list'] == 'pub': #pub인 경우에만 추가..
                    code = version['code']
                    pub_version_list.append(version)
                    print(f"version_list에 {code}가 담겼습니다.")
                    print(pub_version_list)
            return pub_version_list
        except Exception as e:
            print (version)
            print(f"Error retrieving versions: {str(e)}")
            return []
        
    def get_task_step_by_id(self, task_id): #세영 추가함
        """
        주어진 Task ID에 대한 Task Step을 반환합니다.
        

        Args:
            task_id (int): Task의 ID.

        Returns:
            str: Task Step의 이름 또는 None.
        """
        try:
            # Task 정보 가져오기, 여기서 'step' 필드를 포함시킵니다.
            
            task = self.sg.find_one(
                "Task", 
                [["id", "is", task_id]], 
                ["step"]
            )
            print(task)
            if task and task.get("step"):
                return task["step"]["name"]
            else:
                print(f"Task ID {task_id}에 대한 Task Step이 없습니다.")
                return None

        except Exception as e:
            print(f"Task ID {task_id}에 대한 정보를 가져오는데 오류가 발생했습니다: {e}")
            return None
        
        
    def get_standard_aov_info(self,project_id):
        
        fields = ['sg_standard_aovs']  # 'aov'는 실제 필드 이름으로 변경

        # 필터를 통해 특정 프로젝트의 `projectinfo` 엔티티 조회
        filters = [['id', 'is', project_id]]

        # `projectinfo` 엔티티 쿼리
        project_info = self.sg.find_one('Project', filters, fields)
        aovs = project_info.get('sg_standard_aovs')
        aovs_list = aovs.split(",")
        return aovs_list
    #def get_published_file_type_maya(self):

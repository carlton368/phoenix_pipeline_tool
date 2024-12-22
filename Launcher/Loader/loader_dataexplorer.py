import os
import requests
import shutil
# import shotgun_api3
from typing import Optional, List, Dict, Any, Tuple
from Launcher.Loader.loader_config_manager import ConfigManager
from functools import lru_cache
import time


class ThumbnailManager:
    
    def __init__(self, sg, save_dir: str = None):
        self.sg = sg
        config_manager = ConfigManager()
        self.save_dir=save_dir
        if self.save_dir is None:
            self.save_dir = os.path.join(config_manager.get_cache_path(), "project_thumbnails")
        else:
            self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def download_project_thumbnail(self, project_id: int) -> Optional[str]: # 프로젝트 썸네일 다운로드
        """프로젝트 썸네일을 다운로드하거나 로컬 파일을 반환합니다."""
        file_name = f"project_{project_id}_thumbnail.jpg"   # 썸네일 파일 이름
        local_file_path = os.path.join(self.save_dir, file_name)    # 썸네일 파일 경로

        if os.path.exists(local_file_path): # 이미 썸네일 파일이 있으면
            return local_file_path  # 썸네일 파일 경로 반환

        project = self.sg.find_one('Project', [['id', 'is', project_id]], ['image'])    # 프로젝트 정보 조회
        if not project or not project.get('image'): # 프로젝트 정보가 없거나 이미지 정보가 없으면
            return None   # None 반환

        try:
            thumbnail_url = project['image']    # 썸네일 URL
            if not thumbnail_url:   # 썸네일 URL이 없으면
                return None

            self._download_file(thumbnail_url, self.save_dir, file_name)        # 썸네일 다운로드
            return local_file_path
        except Exception as e:
            print(f"프로젝트 썸네일 다운로드 중 오류 발생: {e}")
            return None
    def download_version_thumbnail(self, version_id: int, version_type: str) -> Optional[str]:
        # 메소드 내용...
        """특정 버전의 썸네일을 다운로드하거나 로컬 파일을 반환합니다."""
        base_path = f'{os.path.dirname(os.path.abspath(__file__))}/data_from_loader/version_thumbnail'   # 썸네일 저장 디렉토리
        version_path = os.path.join(base_path, version_type.lower())    # 버전 타입에 따른 디렉토리 경로
        os.makedirs(version_path, exist_ok=True)    # 디렉토리 생성

        version = self.sg.find_one("Version", [['id', 'is', version_id]], ['image', 'code', 'sg_status_list'])  # 버전 정보 조회
        
        if not version: # 버전 정보가 없으면
            print(f"버전 ID {version_id}에 대한 정보를 찾을 수 없습니다.")  
            return None

        if not version.get('image'):    # 이미지 정보가 없으면
            print(f"버전 ID {version_id}에 대한 썸네일을 찾을 수 없습니다.")
            return None

        thumbnail_url = version['image']    # 썸네일 URL
        file_name = f"version{version_id}_thumbnail.jpg"    # 썸네일 파일 이름
        file_path = os.path.join(version_path, file_name)   # 썸네일 파일 경로
        
        if not os.path.exists(file_path):   # 썸네일 파일이 없으면
            try:
                self._download_file(thumbnail_url, version_path, file_name)   # 썸네일 다운로드
                print(f"버전 {version['code']} 썸네일이 {file_path}에 저장되었습니다.")
            except Exception as e:
                print(f"버전 {version['code']} 썸네일 다운로드 중 오류 발생: {e}")  
                return None
        
        return file_path


    def _download_file(self, url: str, save_dir: str, file_name: str) -> None:  # 파일 다운로드
        """주어진 URL에서 파일을 다운로드하여 지정된 디렉토리에 저장합니다."""
        local_file_path = os.path.join(save_dir, file_name)   # 로컬 파일 경로
        try:
            with requests.get(url, stream=True) as response:    # URL에서 파일 다운로드
                response.raise_for_status()
                with open(local_file_path, 'wb') as file:   # 로컬 파일에 저장
                    shutil.copyfileobj(response.raw, file)  # 파일 복사
        except requests.exceptions.RequestException as e:   # 요청 예외 처리
            print(f"파일 다운로드 중 오류 발생: {e}")
            raise


class DataExplorer:
    """
    ShotGrid API를 사용하여 프로젝트, 에셋, 샷 등의 데이터를 탐색하고,
    프로젝트의 썸네일을 다운로드하는 기능을 제공하는 클래스입니다.
    """

    def __init__(self, sg, email):
        """
        DataExplorer 초기화 메서드
        :param email: 사용자 이메일 주소
        """
        # ShotGrid API 연결 설정
        self.sg = sg
        # 썸네일 저장 디렉토리 설정
        self.config = ConfigManager()
        self.data_manager = DataManagerForSaver()  # DataManagerForSaver 클래스 인스턴스화
        self.thumbnail_manager = ThumbnailManager(self.sg)
        # 현재 사용자 정보 가져오기
        self.email= email
        self.user_info = self.get_user_info(email)  # 사용자 정보 조회
        self.schema_cache = {}


    @lru_cache(maxsize=128, typed=False)
    def get_user_tasks(self, project_id: int) -> Tuple[Dict[str, Any]]: 
        """
        프로젝트에서 유저의 모든 태스크를 가져옵니다.
        :param project_id: 프로젝트 ID
        :return: 태스크 정보 튜플
        """
        print(f"Fetching all user tasks for project ID: {project_id}")
        tasks = self.sg.find(
            "Task",
            [
                ['project.Project.id', 'is', project_id],   # 프로젝트 ID
                ['task_assignees', 'is', self.user_info],   # 사용자 정보
                ['sg_status_list', 'in', ['wip', 'pub', 'rtg']] # 태스크 상태
            ],
            [
                "content", "id", "step.Step.code",
                "entity", "project.Project.id", "project.Project.name",
                "sg_status_list"    
            ],  # 필드 목록(태스크 정보)
            order=[{'field_name': 'due_date', 'direction': 'asc'}]  # 정렬(마감일 오름차순)
        )
        
        self.task_groups = {
            'Asset': {},
            'Shot': {}
        }   # 태스크 그룹 초기화
        
        for task in tasks:  # 태스크 그룹화
            entity = task.get('entity') # 엔티티 정보
            if entity:  # 엔티티 정보가 있으면
                entity_type = entity.get('type')    # 엔티티 타입
                entity_name = entity.get('name')    # 엔티티 이름
                if entity_type in self.task_groups: # 엔티티 타입이 태스크 그룹에 있으면
                    if entity_name not in self.task_groups[entity_type]:    # 엔티티 이름이 태스크 그룹에 없으면
                        self.task_groups[entity_type][entity_name] = []   # 빈 리스트 생성
                    self.task_groups[entity_type][entity_name].append(task) # 태스크 추가
            else:
                print(f"Warning: Task {task.get('id')} has no entity information.")
                # 엔티티 정보가 없는 태스크를 별도로 처리하거나 무시할 수 있습니다.
        result = tuple(tasks)
        return result


##############################################################################################################################################################################################################################################   

    
    @lru_cache(maxsize=128, typed=False)
    def get_task_info(self, task_id: int) -> Dict[str, Any]:    # 태스크 정보 가져오기
        print(f"Fetching task info for task ID: {task_id}")
        task_info = self.sg.find_one(
        'Task',
            [['id', 'is', task_id]],    # 필터 설정(태스크 ID)
            [
                'content', 'step.Step.code', 
                'entity.Asset.code', 'entity.Shot.code',
                'project.Project.id', 'project.Project.name',
                'sg_status_list', 'due_date', 
                'task_assignees.HumanUser.name'
            ],  # 필드 목록(태스크 정보)
            order=[{'field_name': 'due_date', 'direction': 'asc'}]
            )   # 정렬(마감일 오름차순)
        return task_info or {}  # 태스크 정보가 없으면 빈 딕셔너리 반환
    
    @lru_cache(maxsize=256, typed=False)
    def get_versions(self, entity_id: int, entity_type: str, task_id: int, project_name: str) -> Tuple[Dict[str, Any]]:  # 버전 가져오기
        print(f"Fetching versions for {entity_type} ID: {entity_id}, task ID: {task_id}")
        """
        특정 엔티티에 대한 버전 정보를 가져옵니다.
        



        """
        versions = self.sg.find(
            'Version',  # 엔티티 유형
            [
                ['project.Project.name', 'is', project_name],   # 프로젝트 이름
                ['entity', 'is', {'type': entity_type, 'id': entity_id}],   # 엔티티 정보 
                ['sg_task', 'is', {'type': 'Task', 'id': task_id}]  # 태스크 정보
            ],  # 필터 설정(프로젝트, 엔티티, 태스크)
            [
                'code', 'sg_status_list', 'created_at',     
                'user.HumanUser.name', 'description', 
                'sg_path_to_frames', 'sg_first_frame', 'sg_last_frame',
                'sg_task.Task.content', f'entity.{entity_type}.code',
                'sg_path', 'sg_version_file_type'
            ],  # 필드 목록(버전 정보)
            order=[{'field_name': 'created_at', 'direction': 'desc'}]   # 정렬(생성일 내림차순)
        )
        result = Tuple(versions)
        return result

    @lru_cache(maxsize=64, typed=False)
    def get_asset_types(self, project_name: str) -> Tuple[str]: # 에셋 타입 가져오기
        """ 프로젝트에 속한 에셋 타입들을 가져옵니다. """
        print(f"Fetching asset types for project: {project_name}")
        asset_types = self.sg.find(
            'Asset',
            [['project.Project.name', 'is', project_name]],   # 프로젝트 이름
            ['sg_asset_type'],  # 필드 목록(에셋 타입)
            group_by=['sg_asset_type']  # 그룹화(에셋 타입)
        )   # 에셋 타입 조회
        # asset_types가 비어있으면, 빈 튜플을 반환하고 함수 종료
        if not asset_types: 
            asset_types = []
            result = tuple(asset_types) # 튜플로 변환
            return result

        all_asset_types = []    # 모든 에셋 타입
        for asset_type in asset_types:  # 에셋 타입 반복
            asset_type.get('sg_asset_type',None)    # 에셋 타입 정보 가져오기


        result = tuple(all_asset_types) # 튜플로 변환
        return result

    @lru_cache(maxsize=128, typed=False)
    def get_assets_by_type(self, project_name: str, asset_type: str) -> Tuple[Dict[str, Any]]:
        """ 프로젝트에 속한 특정 타입의 에셋들을 가져옵니다. """
        print(f"Fetching assets of type {asset_type} for project: {project_name}")
        assets = self.sg.find(
            'Asset',
            [
                ['project.Project.name', 'is', project_name],
                ['sg_asset_type', 'is', asset_type]
            ],
            [
                'code', 'id', 'sg_asset_type', 'sg_status_list',
                'tasks.Task.content', 'tasks.Task.sg_status_list'
            ],
            order=[{'field_name': 'code', 'direction': 'asc'}]
        )  

        if assets:
            result = tuple(assets)
            print(f"Found {len(assets)} assets of type {asset_type}")
        else:
            result = ()
            print(f"No assets found of type {asset_type}")
        return result

    def clear_caches(self):
        self.get_user_tasks.cache_clear()
        self.get_task_info.cache_clear()
        self.get_versions.cache_clear()
        self.get_asset_types.cache_clear()
        self.get_assets_by_type.cache_clear()

    @lru_cache(maxsize=32, typed=False)
    def get_user_info(self, email: str = None) -> Dict[str, Any]:  # 사용자 정보 가져오기
        """
        주어진 이메일 주소를 기반으로 사용자 정보를 가져옵니다.
        :param email: 사용자 이메일 주소
        :return: 사용자 정보 딕셔너리
        """
        print(f"이메일 {email}에 대한 사용자 정보 조회 중...")

        if not email:
            print("이메일 주소가 없습니다.")
            return {"name": "Unknown User", "login": None, "id": None, "sg_step": None}
        
        user = self.sg.find_one("HumanUser",
                                [["email", "is", email]],
                                ["name", "login", "id", "sg_step"]) # 사용자 정보 조회
        
        if user:
            print(f"사용자 정보 찾음: {user['name']}")
            return user
        else:
            print("사용자 정보를 찾을 수 없습니다.")
            return {"name": "Unknown User", "login": email, "id": None, "sg_step": None} # 사용자 정보 없을 시 기본값 반환
    @lru_cache(maxsize=32, typed=False)
    def get_assets(self, project_id: int) -> List[Dict[str, Any]]:  # 에셋 가져오기
        """
        주어진 프로젝트 ID에 속한 에셋 목록을 반환합니다.
        :param project_id: 프로젝트 ID
        :return: 에셋 정보 리스트
        """
        assets = self.sg.find("Asset", [['project', 'is', {'type': 'Project', 'id': project_id}]],
                            ["code", "id", "sg_asset_type"])
        return assets

    
    def get_version_metadata(self, project_id, version_code: str, version_type: str = None) -> Dict[str, Any]:
        print(f"Attempting to retrieve metadata for version: {version_code}, type: {version_type}")
        
        filters = [
            ['project.Project.id', 'is', project_id],
            ['code', 'is', version_code]
        ]
        if version_type:
            filters.append(['sg_status_list', 'is', version_type])
        
        fields = ['code', 'sg_status_list', 'created_at', 'user.HumanUser.name', 'description',  
                'sg_path_to_frames', 'sg_first_frame', 'sg_last_frame', 'sg_task', 'entity', 'sg_path', 'sg_version_file_type',]  
        
        try:
            version = self.sg.find_one('Version', filters, fields)
            if version:
                print(f"Successfully retrieved version metadata: {version}")
                return version
            else:
                print(f"No version found with code: {version_code} and type: {version_type}")
                return {}
        except Exception as e:
            print(f"Error retrieving version metadata: {e}")
            return {}
        
    
        
        
    def get_version_metadata_for_vfx_programs(self, version_code: str, version_type: str = None) -> Dict[str, Any]:  # 버전 메타데이터 가져오기
        print(f"Attempting to retrieve metadata for version: {version_code}, type: {version_type}") # 디버그 로그 추가
        
        filters = [['code', 'is', version_code]]    # 필터 설정
        if version_type:    # 버전 타입이 있으면
            filters.append(['sg_status_list', 'is', version_type])  # 필터 추가
        
        fields = ['code', 'sg_status_list', 'created_at', 'user.HumanUser.name', 'description',  
                'sg_path_to_frames', 'sg_first_frame', 'sg_last_frame', 'sg_task', 'entity', 'sg_path', 'sg_version_file_type',]    
        
        try:
            version = self.sg.find_one('Version', filters, fields)
            if version:
                print(f"Successfully retrieved version metadata: {version}")
                return version
            else:
                print(f"No version found with code: {version_code} and type: {version_type}")
                # 버전 타입을 무시하고 다시 검색
                version = self.sg.find_one('Version', [['code', 'is', version_code]], fields)
                if version:
                    print(f"Found version ignoring type: {version}")
                    return version
                else:
                    print(f"No version found even ignoring type for code: {version_code}")
                    return {}
        except Exception as e:
            print(f"Error retrieving version metadata: {e}")
            return {}
     
    def get_pub_version_data_from_published_files(self, version_id: int) -> Dict[str, Any]:  # pub 상태인 버전의 shotgun puublished files의 데이터 가져오기
        """버전 ID에 해당하는 데이터를 shotgun published files에서 가져옵니다."""
        publish = self.sg.find_one("PublishedFile", 
                                   [["version.Version.id", "is", version_id]], 
                                   ["code", "published_file_type", "version_number", "path", "created_at", "user.HumanUser.name", "description"])
        print("!!!!!!!!!!!!!!!!!!!!버전 ID에 해당하는 데이터를 shotgun publishes에서 가져옵니다!!!!!!!!!!!!!!!!!")    
        return publish if publish else {}
    
    @lru_cache(maxsize=32, typed=False)
    def get_entity_type_from_task(self, task_id: int) -> str:
        if task_id in self.schema_cache:
            return self.schema_cache[task_id]

        task = self.sg.find_one('Task', [['id', 'is', task_id]], ['step'])
        if not task or 'step' not in task:
            return 'Unknown'

        step_id = task['step']['id']
        step = self.sg.find_one('Step', [['id', 'is', step_id]], ['entity_type'])
        
        if not step or 'entity_type' not in step:
            return 'Unknown'

        entity_type = step['entity_type']
        self.schema_cache[task_id] = entity_type
        return entity_type

    @lru_cache(maxsize=32, typed=False)
    def get_projects(self) -> Tuple[Dict[str, Any]]:
        """
        ShotGrid API를 통해 프로젝트 목록을 가져옵니다.
        :return: 프로젝트 정보 리스트 (이름, ID, 상태, 이미지 포함)
        """
        projects = self.sg.find("Project", [], ["name", "id", "sg_status", "image", "sg_project_resolution_width", "sg_project_resolution_height"])
        return tuple(projects)

    @lru_cache(maxsize=32, typed=False)
    def get_sequences(self, project_id: int) -> Tuple[Dict[str, Any]]:
        """
        주어진 프로젝트 ID에 속한 시퀀스 목록을 반환합니다.
        :param project_id: 프로젝트 ID
        :return: 시퀀스 정보 리스트
        """
        sequences = self.sg.find("Sequence", [['project', 'is', {'type': 'Project', 'id': project_id}]],
                                 ["code", "id"])
        return tuple(sequences)
    
    @lru_cache(maxsize=32, typed=False)
    def get_shots_in_sequence(self, sequence_id: int) -> Tuple[Dict[str, Any]]:
        """
        주어진 시퀀스 ID에 속한 샷 목록을 반환합니다.
        :param sequence_id: 시퀀스 ID
        :return: 샷 정보 리스트
        """
        shots = self.sg.find("Shot", [['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}]],
                             ["code", "id"])
        return tuple(shots)


    def get_entity_details(self, entity_type: str, entity_id: int) -> Dict[str, Any]:
        """
        특정 엔티티의 세부 정보를 반환합니다.
        :param entity_type: 엔티티 유형 (예: Asset, Shot)
        :param entity_id: 엔티티 ID
        :return: 엔티티 세부 정보 딕셔너리
        """
        details = self.sg.find_one(entity_type, [["id", "is", entity_id]], ["*"])
        return details

    def get_publishedfile_details(self, entity_type: str, entity_id: int) -> Tuple[Dict[str, Any]]:
        """
        주어진 엔티티(Asset 또는 Shot)와 연관된 Publish 파일들을 반환합니다.
        :param entity_type: 엔티티 유형 (예: Asset, Shot)
        :param entity_id: 엔티티 ID
        :return: Publish 파일 정보 리스트
        """
        publishes = self.sg.find("PublishedFile",
                                 [['entity', 'is', {'type': entity_type, 'id': entity_id}]],
                                 ['code', 'id', 'published_file_type', 'version_number', 'created_at', 'user.HumanUser.name', 'description'])
        return tuple(publishes)

    def get_shot_versions(self, shot_id: int) -> List[Dict[str, Any]]:
        """
        주어진 shot ID에 대한 version 정보를 가져옵니다.
        :param shot_id: Shot의 ID
        :return: Version 정보 리스트
        """
        print(f"Shot ID {shot_id}에 대한 version 정보 조회 중...")
        versions = self.sg.find("Version",
                                [["entity", "is", {"type": "Shot", "id": shot_id}]],
                                ["code","sg_status_list", "id"])
        print(f"{len(versions)}개의 version 정보를 찾았습니다.")
        return versions
##############################################################################################################################################################################################################################################
    def get_shot_tasks(self, project_id: int) -> Dict[str, List[Dict[str, Any]]]:
        """프로젝트의 모든 샷에 대한 태스크 목록을 가져옵니다."""
        filename = f'shot_tasks_{project_id}.json'
        cached_data = self.data_manager.load_data(filename)
        if cached_data:
            return cached_data

        tasks = self.sg.find("Task", 
                             [['project', 'is', {'type': 'Project', 'id': project_id}],
                              ['entity.Shot.code', 'is_not', None]],
                             ['content', 'entity', 'step', 'id'])
        
        shot_tasks = {}
        for task in tasks:
            shot_code = task['entity']['name']
            if shot_code not in shot_tasks:
                shot_tasks[shot_code] = []
            shot_tasks[shot_code].append({
                'content': task['content'],
                'step': task['step']['name'] if task['step'] else 'Unknown',
                'id': task['id']
            })

        self.data_manager.save_data(shot_tasks, filename)
        return shot_tasks
        
    def get_asset_tasks(self, project_id: int) -> Dict[str, List[Dict[str, Any]]]:
        """프로젝트의 모든 Asset에 대한 태스크 목록을 가져옵니다."""
        filename = f'asset_tasks_{project_id}.json'
        cached_data = self.data_manager.load_data(filename)
        if cached_data:
            return cached_data

        tasks = self.sg.find("Task", 
                             [['project', 'is', {'type': 'Project', 'id': project_id}],
                              ['entity.Asset.code', 'is_not', None]],
                             ['content', 'entity', 'step', 'id'])

        asset_tasks = {}
        for task in tasks:
            asset_code = task['entity']['name']
            if asset_code not in asset_tasks:
                asset_tasks[asset_code] = []
            asset_tasks[asset_code].append({
                'content': task['content'],
                'step': task['step']['name'] if task['step'] else 'Unknown',
                'id': task['id']
            })
        self.data_manager.save_data(asset_tasks, filename)
        return asset_tasks
    
    def get_version(self, task_id: int) -> List[Dict[str, Any]]:
        print(f"Debug - Getting versions for task ID: {task_id}")
        versions = self.sg.find("Version", 
                                [['sg_task', 'is', {'type': 'Task', 'id': task_id}]], 
                                ["code", "sg_status_list", "id", "created_at"])
        print(f"Debug - Raw versions data from ShotGrid: {versions}")
        return versions

    def get_entity_type_from_schema(self, entity_id):
        try:
            entity = self.sg.find_one('Entity', [['id', 'is', entity_id]], ['type'])
            if not entity:
                return None
            
            entity_type = entity['type']
            schema = self.sg.schema_field_read(entity_type)
            
            if 'sg_sequence' in schema:  # Shot에만 있는 필드
                return 'Shot'
            elif 'sg_asset_type' in schema:  # Asset에만 있는 필드
                return 'Asset'
            else:
                return None
        except Exception as e:
            print(f"Error getting entity type from schema: {e}")
            return None
    def create_new_version(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new version in Shotgun."""
        try:
            new_version = self.sg.create('Version', data)
            print(f"New version created: {new_version['code']}")
            return new_version
        except Exception as e:
            print(f"Error creating new version: {e}")
            return {}
            
import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

class DataManagerForSaver:
    """
    데이터 캐싱을 관리하는 싱글톤 클래스입니다.
    이 클래스는 JSON 형식의 데이터를 저장하고 로드하는 기능을 제공합니다.
    """
    _instance = None
    ROOT_PATH = None  # 클래스 변수로 ROOT_PATH 정의

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            config_manager = ConfigManager()
            base_path = config_manager.get_base_path()
            cls._instance.ROOT_PATH = os.path.join(base_path, 'Launcher', 'Loader', 'data_from_loader')
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self):
        """
        인스턴스를 초기화합니다.
        캐시 디렉토리 경로를 설정합니다.
        """
        self.cache_dir = self.ROOT_PATH

    def _ensure_directory_exists(self):
        """
        캐시 디렉토리가 존재하는지 확인하고, 없으면 생성합니다.
        이 메서드는 데이터를 저장하기 전에 호출되어 디렉토리 존재를 보장합니다.
        """
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
        except OSError as e:
            print(f"캐시 디렉토리 생성 중 오류 발생: {e}")

    def save_data(self, data: Any, filename: str) -> None:
        """
        데이터를 JSON 파일로 저장합니다.
        
        :param data: 저장할 데이터 (Any 타입)
        :param filename: 저장할 파일 이름
        """
        self._ensure_directory_exists()  # 디렉토리 존재 확인
        file_path = os.path.join(self.cache_dir, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # 데이터를 타임스탬프와 함께 저장
                json.dump({'timestamp': datetime.now().isoformat(), 'data': data}, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"데이터 저장 중 오류 발생: {e}")

    def load_data(self, filename: str) -> Optional[Any]:
        """
        JSON 파일에서 데이터를 로드합니다.
        
        :param filename: 로드할 파일 이름
        :return: 로드된 데이터 또는 None (파일이 없거나 오류 발생 시)
        """
        file_path = os.path.join(self.cache_dir, filename)
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                return cache['data']  # 'data' 키에 저장된 실제 데이터만 반환
        except (IOError, json.JSONDecodeError) as e:
            print(f"데이터 로드 중 오류 발생: {e}")
        return None

    def clear_cache(self) -> None:
        """
        모든 캐시 파일을 삭제합니다.
        캐시 디렉토리 내의 모든 파일을 순회하며 삭제를 시도합니다.
        """
        if os.path.exists(self.cache_dir):
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if filename.startswith('json'):
                    print(f'json으로 시작하는 파일은 건너뜁니다: {file_path}')
                    continue
                
                try:
                    if os.path.isfile(file_path):
                        print(f'필요없는 파일을 지웁니다: {file_path}')
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        print(f'필요없는 폴더를 지웁니다: {file_path}')
                        shutil.rmtree(file_path)
                    else:
                        print(f'알 수 없는 파일 형식입니다: {file_path}')
                except Exception as e:
                    print(f"삭제 중 오류 발생: {file_path}, 오류: {e}")
        else:
            print(f"캐시 디렉토리가 존재하지 않습니다: {self.cache_dir}")

    def save_data_for_saver(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        데이터를 JSON 파일로 저장합니다. 
        이 메서드는 특별히 'json_from_loader.json' 파일에 데이터를 저장합니다.
        
        :param data: 저장할 데이터 (기본값은 None, None일 경우 빈 딕셔너리 사용)
        """
        if data is None:
            data = {}
        
        if not isinstance(data, dict):
            print("오류: 데이터는 딕셔너리 형태여야 합니다.")
            return

        self._ensure_directory_exists()
        file_path = os.path.join(self.cache_dir, 'json_from_loader.json')
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"데이터가 성공적으로 저장되었습니다: {file_path}")
        except IOError as e:
            print(f"데이터 저장 중 오류 발생: {e}")



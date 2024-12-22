# import nuke
# from shotgun_api3 import Shotgun
# import re
# import os
# import sys

# class DataExploreForSceneSetting:
#     """
#     Scene 셋팅에 필요한 정보를 불러오는 모듈입니다.
#     """
#     def __init__(self):
#         self.sg = Shotgun("https://4thacademy.shotgrid.autodesk.com",
#                           "kangseyoung",
#                           "imthtqts8zqqXylfckoiihx-z")
        
#     ################################################################################################################
         
#     def get_current_file_path(self):    # 현재 파일 경로 받기
#         """
#         현재 열려 있는 Nuke 파일의 경로를 반환합니다.
        
#         :return: 파일 경로 문자열 (파일이 저장되지 않았으면 빈 문자열 반환)
#         """
#         return nuke.root().name()
    
#     def get_shotgrid_directory(self, current_path):   # 현재 경로에서 샷그리드 관련 경로 찾기
#         root_folder = "/phoenix_pipeline_folders/"
#         p = re.compile(rf"{root_folder}(.+?)/(Shots|Assets)/(.+?)/[^/]+$")
#         p_data = p.search(current_path)
#         if p_data:
#             extracted_path = os.path.join(p_data.group(1), p_data.group(3))
#         return extracted_path
    
#     def get_project_by_name(self, project_name:str):    # 이름으로 프로젝트 정보 받기
#         """
#         ShotGrid에서 프로젝트 이름을 기반으로 프로젝트 정보를 가져옵니다.
#         :return: 프로젝트 정보 딕셔너리 (존재하지 않으면 None)
#         """
#         # ShotGrid에서 프로젝트 검색
#         project = self.sg.find_one('Project',
#                                    [['name', 'is', project_name]], 
#                                    ['id', 'name'])
#         return project
        
#     def get_sequence_by_name(self, project_id: int, sequence_name: str):    # 시퀀스 이름으로 시퀀스 정보받기
#         """
#         프로젝트 ID와 시퀀스 이름을 사용해 시퀀스 정보를 가져옵니다.
#         return: 시퀀스 정보가 포함된 딕셔너리 (없으면 None 반환)
#         """
#         # 시퀀스를 조회하기 위한 필터 설정
#         filters = [['project', 'is', {'type': 'Project', 'id': project_id}],
#             ['code', 'is', sequence_name]]
        
#         # ShotGrid에서 시퀀스 정보를 가져오기
#         sequence = self.sg.find_one("Sequence", filters, ['id', 'code', 'description', 'sg_status_list', 'created_at'])
        
#         return sequence
    
#     def get_shot_by_name(self, sequence_id: int, shot_name: str):   # 샷 이름으로 샷 정보받기
#         """
#         시퀀스 ID와 샷 이름을 사용해 샷 정보를 가져옵니다.
#         return: 샷 정보가 포함된 딕셔너리 (없으면 None 반환)
#         """
#         # 샷을 조회하기 위한 필터 설정
#         filters = [['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}],
#             ['code', 'is', shot_name]]
        
#         # ShotGrid에서 샷 정보를 가져오기
#         shot = self.sg.find_one("Shot", filters, ['id', 'code', 'description', 'sg_status_list', 'created_at', 'sg_sequence'])
        
#         return shot
    
#     ################################################################################################################
    
#     def extract_path_info(self):    # 현재 파일 경로로 필요한 entity id 받기 ++Asset
#         current_path = self.get_current_file_path()
#         # 현재 경로로 project 이름, sequence 이름, shot 이름찾기.
#         shotgrid_directory = self.get_shotgrid_directory(current_path)
#         proj_name = shotgrid_directory.split('/')[0]
#         seq_name = shotgrid_directory.split('/')[1]
#         shot_name = shotgrid_directory.split('/')[2]
#         task_name = shotgrid_directory.split('/')[3]
        
#         project_dic = self.get_project_by_name(proj_name)
#         project_id = project_dic['id']
#         sequence_dic  = self.get_sequence_by_name(project_id, seq_name)
#         seq_id = sequence_dic['id']

        
#         # 필요한 정보 저장
#         path_info = {}
#         path_info['project_id'] = project_id
#         path_info['sequence_id'] = seq_id
#         path_info['shot_name'] = shot_name
#         path_info['task_name'] = task_name
        
#         return path_info
        
#     def get_undistortion_dimensions(self):  # 샷의 언디스토션 사이즈 받기 ++Asset
#         """
#         ShotGrid에서 샷 이름과 시퀀스 ID를 기반으로 언디스토션 해상도 값을 가져옵니다.
#         :return: 언디스토션 해상도 딕셔너리 {'width': int, 'height': int} 또는 None
#         """
#         path_info = self.extract_path_info()
#         project_id = path_info['project_id']
#         sequence_id = path_info['sequence_id']
#         shot_name = path_info['shot_name']
        
#         # 샷 필터 설정
#         filters = [
#             ['code', 'is', shot_name],  # 샷 이름 필터
#             ['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}],  # 시퀀스 ID 필터
#             ['project', 'is', {'type': 'Project', 'id': project_id}]  # 프로젝트 ID 필터
#         ]

#         # 가져올 필드 목록 설정
#         fields = ['sg_undistortion_width', 'sg_undistortion_height']
        
#         # ShotGrid에서 샷 검색
#         shot = self.sg.find_one('Shot', filters, fields)
        
#         if shot and shot['sg_undistortion_width'] and shot['sg_undistortion_height']:
#             return {'width': shot['sg_undistortion_width'],
#                     'height': shot['sg_undistortion_height']}
#         else:
#             print(f"Shot '{shot_name}' in sequence ID {sequence_id} not found or missing undistortion data.")
#             return None
    
#     def get_camera_alembic_cache(self): # 샷의 카메라 alembic cache 가져오기 ++Comp
#         """
#         ShotGrid에서 샷 이름과 시퀀스 ID를 기반으로 카메라 alembic cache를 가져옵니다.
#         """
#         print('get_camera_alembic_cache, start')
#         path_info = self.extract_path_info()
#         project_id = path_info['project_id']
#         sequence_id = path_info['sequence_id']
#         shot_name = path_info['shot_name']
        
#         # 샷 필터 설정
#         filters = [
#             ['code', 'is', shot_name],  # 샷 이름 필터
#             ['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}],  # 시퀀스 ID 필터
#             ['project', 'is', {'type': 'Project', 'id': project_id}]  # 프로젝트 ID 필터
#         ]

#         # 가져올 필드 목록 설정
#         fields = ['sg_camera_cache_path']
        
#         # ShotGrid에서 샷 검색
#         shot = self.sg.find_one('Shot', filters, fields)
        
#         if shot and shot['sg_camera_cache_path']:
#             return shot['sg_camera_cache_path']
                    
#         else:
#             print(f"Shot '{shot_name}' in sequence ID {sequence_id} not found or missing camera cache path.")
#             return None



import nuke
from shotgun_api3 import Shotgun
import re
import os
import sys

class DataExploreForSceneSetting:
    """
    Scene 셋팅에 필요한 정보를 불러오는 모듈입니다.
    """
    def __init__(self):
        self.sg = Shotgun("https://4thacademy.shotgrid.autodesk.com",
                          "kangseyoung",
                          "imthtqts8zqqXylfckoiihx-z")
        
    ################################################################################################################
         
    def get_current_file_path(self):    # 현재 파일 경로 받기
        """
        현재 열려 있는 Nuke 파일의 경로를 반환합니다.
        
        :return: 파일 경로 문자열 (파일이 저장되지 않았으면 빈 문자열 반환)
        """
        return nuke.root().name()
    
    def get_shotgrid_directory(self, current_path):   # 현재 경로에서 샷그리드 관련 경로 찾기
        root_folder = "/phoenix_pipeline_folders/"
        p = re.compile(rf"{root_folder}(.+?)/(Shots|Assets)/(.+?)/[^/]+$")
        p_data = p.search(current_path)
        if p_data:
            extracted_path = os.path.join(p_data.group(1), p_data.group(3))
        return extracted_path
    
    def get_project_by_name(self, project_name:str):    # 이름으로 프로젝트 정보 받기
        """
        ShotGrid에서 프로젝트 이름을 기반으로 프로젝트 정보를 가져옵니다.
        :return: 프로젝트 정보 딕셔너리 (존재하지 않으면 None)
        """
        # ShotGrid에서 프로젝트 검색
        project = self.sg.find_one('Project',
                                   [['name', 'is', project_name]], 
                                   ['id', 'name'])
        return project
        
    def get_sequence_by_name(self, project_id: int, sequence_name: str):    # 시퀀스 이름으로 시퀀스 정보받기
        """
        프로젝트 ID와 시퀀스 이름을 사용해 시퀀스 정보를 가져옵니다.
        return: 시퀀스 정보가 포함된 딕셔너리 (없으면 None 반환)
        """
        # 시퀀스를 조회하기 위한 필터 설정
        filters = [['project', 'is', {'type': 'Project', 'id': project_id}],
            ['code', 'is', sequence_name]]
        
        # ShotGrid에서 시퀀스 정보를 가져오기
        sequence = self.sg.find_one("Sequence", filters, ['id', 'code', 'description', 'sg_status_list', 'created_at'])
        
        return sequence
    
    def get_shot_by_name(self, sequence_id: int, shot_name: str):   # 샷 이름으로 샷 정보받기
        """
        시퀀스 ID와 샷 이름을 사용해 샷 정보를 가져옵니다.
        return: 샷 정보가 포함된 딕셔너리 (없으면 None 반환)
        """
        # 샷을 조회하기 위한 필터 설정
        filters = [['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}],
            ['code', 'is', shot_name]]
        
        # ShotGrid에서 샷 정보를 가져오기
        shot = self.sg.find_one("Shot", filters, ['id', 'code', 'description', 'sg_status_list', 'created_at', 'sg_sequence'])
        
        return shot
    
    ################################################################################################################
    
    def extract_path_info(self):    # 현재 파일 경로로 필요한 entity id 받기 ++Asset
        current_path = self.get_current_file_path()
        # 현재 경로로 project 이름, sequence 이름, shot 이름찾기.
        shotgrid_directory = self.get_shotgrid_directory(current_path)
        proj_name = shotgrid_directory.split('/')[0]
        seq_name = shotgrid_directory.split('/')[1]
        shot_name = shotgrid_directory.split('/')[2]
        task_name = shotgrid_directory.split('/')[3]
        
        project_dic = self.get_project_by_name(proj_name)
        project_id = project_dic['id']
        sequence_dic  = self.get_sequence_by_name(project_id, seq_name)
        seq_id = sequence_dic['id']

        
        # 필요한 정보 저장
        path_info = {}
        path_info['project_id'] = project_id
        path_info['sequence_id'] = seq_id
        path_info['shot_name'] = shot_name
        path_info['task_name'] = task_name
        
        return path_info
        
    def get_undistortion_dimensions(self):  # 샷의 언디스토션 사이즈 받기 ++Asset
        """
        ShotGrid에서 샷 이름과 시퀀스 ID를 기반으로 언디스토션 해상도 값을 가져옵니다.
        :return: 언디스토션 해상도 딕셔너리 {'width': int, 'height': int} 또는 None
        """
        path_info = self.extract_path_info()
        project_id = path_info['project_id']
        sequence_id = path_info['sequence_id']
        shot_name = path_info['shot_name']
        
        # 샷 필터 설정
        filters = [
            ['code', 'is', shot_name],  # 샷 이름 필터
            ['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}],  # 시퀀스 ID 필터
            ['project', 'is', {'type': 'Project', 'id': project_id}]  # 프로젝트 ID 필터
        ]

        # 가져올 필드 목록 설정
        fields = ['sg_undistortion_width', 'sg_undistortion_height']
        
        # ShotGrid에서 샷 검색
        shot = self.sg.find_one('Shot', filters, fields)
        
        if shot and shot['sg_undistortion_width'] and shot['sg_undistortion_height']:
            return {'width': shot['sg_undistortion_width'],
                    'height': shot['sg_undistortion_height']}
        else:
            print(f"Shot '{shot_name}' in sequence ID {sequence_id} not found or missing undistortion data.")
            return None
    
    def get_camera_alembic_cache(self): # 샷의 카메라 alembic cache 가져오기 ++Comp
        """
        ShotGrid에서 샷 이름과 시퀀스 ID를 기반으로 카메라 alembic cache를 가져옵니다.
        """
        print('get_camera_alembic_cache, start')
        path_info = self.extract_path_info()
        project_id = path_info['project_id']
        sequence_id = path_info['sequence_id']
        shot_name = path_info['shot_name']
        
        # 샷 필터 설정
        filters = [
            ['code', 'is', shot_name],  # 샷 이름 필터
            ['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}],  # 시퀀스 ID 필터
            ['project', 'is', {'type': 'Project', 'id': project_id}]  # 프로젝트 ID 필터
        ]

        # 가져올 필드 목록 설정
        fields = ['sg_camera_cache_path']
        
        # ShotGrid에서 샷 검색
        shot = self.sg.find_one('Shot', filters, fields)
        
        if shot and shot['sg_camera_cache_path']:
            return shot['sg_camera_cache_path']
                    
        else:
            print(f"Shot '{shot_name}' in sequence ID {sequence_id} not found or missing camera cache path.")
            return None
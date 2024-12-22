
import os
import datetime
print("실행됨!!")

import maya.cmds as cmds

# 마야에서 턴테이블(화이트배경, 조명, 애니 키)세팅해주는 코드
# 수정 사항 : 컬러체크박스 없앴음, _geo를 _grp로 수정
class PlayblastSceneSetter:
    def __init__(self):
        self.file_path ="/home/rapa/_phoenix_/Publisher/Maya/playblast/white_bg_v2.mb"


    # white_bg.mb 파일 임포트
    def import_file(self):
        if os.path.exists(self.file_path):
            cmds.file(self.file_path, i=True, ra=True, mergeNamespacesOnClash=False, namespace=":", options="v=0;", pr=True)
            print("파일이 임포트되었습니다.")
        else:
            print("파일을 찾을 수 없습니다.")
            return False
        return True

    # white_bg.mb의 쉐이더 찾기
    def check_shader_exists(self, shader_name):
        shader_exists = cmds.objExists(shader_name)
        if shader_exists:
            print("쉐이더를 찾았습니다.")
        else:
            print("쉐이더를 찾을 수 없습니다.")
        return shader_exists
    
    # 쉐이더 가져오기
    def import_shaders(self, shader_names):
        if self.import_file():
            for shader_name in shader_names:
                self.check_shader_exists(shader_name)
                
    def set_aces_color_management(self):
    # 색상 관리 활성화
        cmds.colorManagementPrefs(e=True, cmEnabled=True)
        
        # 워킹 스페이스를 ACES로 설정
        cmds.colorManagementPrefs(e=True, renderingSpaceName='ACES - ACEScg')
        
        # 뷰포트의 뷰 트랜스폼을 ACES sRGB로 설정
        cmds.colorManagementPrefs(e=True, viewTransformName='ACES 1.0 SDR-video')
        
        # 렌더링 출력 색공간 설정 (ACEScg 출력)
        cmds.setAttr('defaultRenderGlobals.outputColorSpace', 'ACES - ACEScg', type='string')
        
        print("ACES color management settings applied.")

    # grp그룹 "rt_gr"로 한 번 더 그룹
    def group_geo_objects(self):
        geo_groups = cmds.ls("*_grp", type="transform") ###############수정 필요..
        
        if geo_groups:
            new_group = cmds.group(geo_groups, name="rt_gr")
            
            print("그룹화했습니다.!")
            return new_group
        else:
            print("_grp 그룹을 찾을 수 없습니다.!")
            return None

    # "rt_gr" Y축으로 360도 돌 수 있게 애니 키 설정
    def animate_rotation(self, group_name, start_frame=1, end_frame=200, rotation_angle=360):
        if cmds.objExists(group_name):
            cmds.setKeyframe(group_name, attribute="rotateY", value=0, t=start_frame)
            cmds.setKeyframe(group_name, attribute="rotateY", value=rotation_angle, t=end_frame)
            cmds.selectKey(group_name, time=(start_frame, end_frame), attribute='rotateY')
            cmds.keyTangent(inTangentType="linear", outTangentType="linear")
            print("애니메이션이 설정되었습니다.")
        else:
            print(f"그룹 '{group_name}'를 찾을 수 없습니다.")
    
    # 뷰포트 패널에서 displayLights, displayLights 활성화
    def use_all_lights_and_shadows(self):
        model_panels = cmds.getPanel(type="modelPanel")
        if model_panels:
            for panel in model_panels:
                cmds.modelEditor(panel, e=True, displayLights="all")
                cmds.modelEditor(panel, e=True, shadows=True)
            print("조명과 그림자가 활성화되었습니다.")
        else:
            print("활성화가 되지 않습니다")

    # 에셋에 위치와 크기에 따라 카메라 생성
    def create_camera(self, main_group):
        if cmds.objExists(main_group):
            
             # 바운딩 박스 계산
            bounding_box = cmds.exactWorldBoundingBox(main_group)
            center_x = (bounding_box[0] + bounding_box[3]) / 2
            center_y = (bounding_box[1] + bounding_box[4]) / 2
            center_z = (bounding_box[2] + bounding_box[5]) / 2

            # 크기 계산
            width = bounding_box[3] - bounding_box[0]
            height = bounding_box[4] - bounding_box[1]
            depth = bounding_box[5] - bounding_box[2]

            # 카메라 거리 계산 1.5배
            distance = max(width, height, depth) * 2.5

            # 새로운 카메라 생성
            camera_name = cmds.camera(name="turntable_camera")[0]

            # 카메라 위치 설정
            cmds.setAttr(f"{camera_name}.translateX", center_x)
            cmds.setAttr(f"{camera_name}.translateY", center_y)
            cmds.setAttr(f"{camera_name}.translateZ", center_z + distance)

            # 카메라가 그룹의 중심을 바라보도록 설정
            cmds.viewPlace(camera_name, lookAt=(center_x, center_y, center_z))

            print("카메라가 생성되었습니다.")
            return camera_name
        else:
            print(f"'{main_group}'를 찾을 수 없습니다.")
            return None

    def get_main_ctrl(self):
        all_curves = cmds.ls(type='nurbsCurve')
        print(all_curves)
        for curve in all_curves:
            if curve == "*ALL_ctrl":
                print(curve)
        return "Ruby_ALL_ctrl"
    
    def run_playblast_setup(self):
        # 1. 파일 임포트
        if not self.import_file():
            return
        shaders = ["white_bg_lb"] 
        self.import_shaders(shaders)
        print("2. 쉐이더 임포트 (필요한 쉐이더 리스트 추가)")

        # 3. 지오메트리 그룹화
        group_name = self.group_geo_objects()
        self.animate_rotation(group_name)
        camera_name = self.create_camera(group_name)
        if not camera_name:
            return
        print(" # 3. 지오메트리 그룹화")  
        if not group_name:
            return print("그룹이름이 없습니다.")
        # 4. 회전 애니메이션 설정
        print("# 4. 회전 애니메이션 설정")
        # 5. 조명과 그림자 활성화
        self.use_all_lights_and_shadows()
        print("#  5. 조명과 그림자 활성화=")
        # 7. 라이트 높이 조정 (예: 'key_light' 이름의 라이트가 있는 경우)
        print("# 7. 라이트 높이 조정 (예: 'key_light' 이름의 라이트가 있는 경우)")

    

        
        
    def run_playblast_setup_for_rig(self):
        # 1. 파일 임포트
        if not self.import_file():
            return
        shaders = ["white_bg_lb"] 
        self.import_shaders(shaders)
        print("2. 쉐이더 임포트 (필요한 쉐이더 리스트 추가)")

        # 3. 지오메트리 그룹화
        main_ctrl = self.get_main_ctrl()
        self.animate_rotation(main_ctrl)
        
        camera_name = self.create_camera(main_ctrl)
        if not camera_name:
            return 
        print(" # 3. 지오메트리 그룹화")  
        if not main_ctrl:
            return print("그룹이름이 없습니다.")
        # 4. 회전 애니메이션 설정
        print("# 4. 회전 애니메이션 설정")
        # 5. 조명과 그림자 활성화
        self.use_all_lights_and_shadows()
        print("#  5. 조명과 그림자 활성화=")
        # 7. 라이트 높이 조정 (예: 'key_light' 이름의 라이트가 있는 경우)
        print("# 7. 라이트 높이 조정 (예: 'key_light' 이름의 라이트가 있는 경우)")   

# import datetime
# print("실행됨!!")

# import maya.cmds as cmds
# class PlayblastSceneSetter:
#     def __init__(self):
#         self.file_path ="/home/rapa/_phoenix_/Publisher/Maya/playblast/white_bg.mb"

#     def import_file(self):
#         if os.path.exists(self.file_path):
#             cmds.file(self.file_path, i=True, ra=True, mergeNamespacesOnClash=False, namespace=":", options="v=0;", pr=True)
#             print("파일이 임포트되었습니다.")
#         else:
#             print("파일을 찾을 수 없습니다.")
#             return False
#         return True

#     def check_shader_exists(self, shader_name):
#         shader_exists = cmds.objExists(shader_name)
#         if shader_exists:
#             print(f"쉐이더 '{shader_name}'를 찾았습니다.")
#         else:
#             print(f"쉐이더 '{shader_name}'를 찾을 수 없습니다.")
#         return shader_exists

#     def import_shaders(self, shader_names):
#         if self.import_file():
#             for shader_name in shader_names:
#                 self.check_shader_exists(shader_name)

#     def group_geo_objects(self):
#         geo_groups = cmds.ls("*_geo", type="transform") ###############수정 필요..
        
#         if geo_groups:
#             new_group = cmds.group(geo_groups, name="rt_gr")
            
#             print("그룹화했습니다.!")
#             return new_group
#         else:
#             print("_geo 그룹을 찾을 수 없습니다.!")
#             return None

#     def animate_rotation(self, group_name, start_frame=1, end_frame=200, rotation_angle=360):
#         if cmds.objExists(group_name):
#             cmds.setKeyframe(group_name, attribute="rotateY", value=0, t=start_frame)
#             cmds.setKeyframe(group_name, attribute="rotateY", value=rotation_angle, t=end_frame)
#             cmds.selectKey(group_name, time=(start_frame, end_frame), attribute='rotateY')
#             cmds.keyTangent(inTangentType="linear", outTangentType="linear")
#             print("애니메이션이 설정되었습니다.")
#         else:
#             print(f"그룹 '{group_name}'를 찾을 수 없습니다.")
    
#     def use_all_lights_and_shadows(self):
#         model_panels = cmds.getPanel(type="modelPanel")
#         if model_panels:
#             for panel in model_panels:
#                 cmds.modelEditor(panel, e=True, displayLights="all")
#                 cmds.modelEditor(panel, e=True, shadows=True)
#             print("조명과 그림자가 활성화되었습니다.")
#         else:
#             print("모델 패널을 찾을 수 없습니다.")

#     def create_camera(self, main_group, additional_object):
#         if cmds.objExists(main_group) and cmds.objExists(additional_object):
#             combined_group = cmds.group(main_group, additional_object, name="combined_group")
            
#             bounding_box = cmds.exactWorldBoundingBox(combined_group)
#             center_x = (bounding_box[0] + bounding_box[3]) / 2
#             center_y = (bounding_box[1] + bounding_box[4]) / 2
#             center_z = (bounding_box[2] + bounding_box[5]) / 2

#             width = bounding_box[3] - bounding_box[0]
#             height = bounding_box[4] - bounding_box[1]
#             depth = bounding_box[5] - bounding_box[2]

#             distance = max(width, height, depth) * 1.5

#             camera_name = cmds.camera(name="turntable_camera")[0]

#             cmds.setAttr(f"{camera_name}.translateX", center_x)
#             cmds.setAttr(f"{camera_name}.translateY", center_y)
#             cmds.setAttr(f"{camera_name}.translateZ", center_z + distance)

#             cmds.viewPlace(camera_name, lookAt=(center_x, center_y, center_z))

#             print("카메라가 생성되었습니다.")
#             return camera_name
#         else:
#             print(f"'{main_group}' 또는 '{additional_object}'를 찾을 수 없습니다.")
#             return None

#     def run_playblast_setup(self):
#         # 1. 파일 임포트
#         if not self.import_file():
#             return
#         shaders = ["white_bg_lb", "color_cherk_board_lb"] 
#         self.import_shaders(shaders)
#         print("2. 쉐이더 임포트 (필요한 쉐이더 리스트 추가)")

#         # 3. 지오메트리 그룹화
#         group_name = self.group_geo_objects()
#         self.animate_rotation(group_name)
#         camera_name = self.create_camera(group_name, "combined_group")
#         if not camera_name:
#             return
#         print(" # 3. 지오메트리 그룹화")  
#         if not group_name:
#             return print("그룹이름이 없습니다.")
#         # 4. 회전 애니메이션 설정
#         print("# 4. 회전 애니메이션 설정")
#         # 5. 조명과 그림자 활성화
#         self.use_all_lights_and_shadows()
#         print("#  5. 조명과 그림자 활성화=")
#         # 7. 라이트 높이 조정 (예: 'key_light' 이름의 라이트가 있는 경우)
#         print("# 7. 라이트 높이 조정 (예: 'key_light' 이름의 라이트가 있는 경우)")
        

import maya.cmds as cmds
import sys
# sys.path.append("/home/rapa/phoenix/phoenix_pipeline_folders/phoenix_pipeline/")

class ValidationCheckForMaya():
    """
    Publisher 에서 Maya 파일에 대한 유효성 검사를 진행하는 클래스입니다.
    """

    print('--Validation Check--')
        
    def check_all_non_quads(self):  # 장면 내 모든 메쉬에서 사각형이 아닌 폴리곤 검사하기
        """
        장면 내의 모든 메쉬에서 사각형이 아닌 폴리곤을 검사합니다.
        """
        # 장면 내 모든 메쉬 가져오기
        meshes = cmds.ls(type='mesh', long=True)

        if not meshes:
            non_quads = []
            validity = True
            pass

        non_quads = []
        for mesh in meshes:
            # 메쉬의 폴리곤 면 가져오기
            # 메쉬의 부모 노드를 가져와야 함
            transform = cmds.listRelatives(mesh, parent=True)[0]
            faces = cmds.ls(cmds.polyListComponentConversion(transform, toFace=True), flatten=True)

            if not faces:
                continue
            
            # 면 정보에서 각 면의 정점 수 검사
            for face in faces:
                # 면의 정점 수를 계산하기 위해 face를 vertex로 변환
                vertices = cmds.polyListComponentConversion(face, toVertex=True)
                num_vertices = len(cmds.ls(vertices, flatten=True))
                # 폴리곤의 정점 수가 4가 아닌 경우
                if num_vertices != 4:
                    non_quads.append(face)

        if non_quads:
            cmds.warning(f"사각형이 아닌 폴리곤이 발견되었습니다: {', '.join(non_quads)}")
            validity = False
        else:
            print('모든 폴리곤이 사각형 입니다.')
            # cmds.confirmDialog(title='검사 완료', message='모든 폴리곤이 사각형입니다.', button=['OK'])
            validity = True
        
        return non_quads, validity

    def list_unused_materials(self, default_materials=None):    # 씬에서 사용되지 않는 재질을 리스트로 반환
        """
        씬에서 사용되지 않는 재질을 리스트로 반환합니다.
        
        :param default_materials: 기본 재질 목록. 삭제하지 않을 재질들을 포함합니다.
        :return: 사용되지 않는 재질의 리스트
        """
        validity = True
        if default_materials is None:
            default_materials = ['lambert1', 'standardSurface1', 'particleCloud1']
        
        # 씬 내 모든 메쉬 오브젝트 가져오기
        all_meshes = cmds.ls(type='mesh')
        
        used_materials = set()
        # 모든 메쉬에 대해 재질을 확인
        for mesh in all_meshes:
            # 메쉬에서 연결된 쉐이딩 엔진(Shading Engine)을 가져옴
            shading_engines = cmds.listConnections(mesh, type = 'shadingEngine')
            
            # 쉐이딩 엔진에서 연결된 재질을 가져옴
            if shading_engines:
                materials = cmds.listConnections(shading_engines[0] + ".surfaceShader")
                used_materials.update(materials)
        
        # 사용되지 않은 재질 찾기
        all_materials = cmds.ls(materials=True)
        unused_materials = list(set(all_materials) - set(default_materials) - used_materials)
        print(f"Unused Materials : {unused_materials}")
        if unused_materials:
            validity = False
        return unused_materials, validity
        
    def delete_unused_materials(self):  # 씬에서 사용되지 않는 재질을 삭제 # mod, rig 외 사용 금지!!!!!!
        
        
        


        """
        씬에서 사용되지 않는 재질을 삭제합니다.
        """
        unused_materials = self.list_unused_materials()
        
        if not unused_materials:
            print('사용되지 않는 재질이 없습니다')
            # cmds.confirmDialog(title='완료', message='사용되지 않는 재질이 없습니다.', button=['OK'])
            return
        
        for material in unused_materials:
            cmds.delete(material)
            print(f"삭제된 재질: {material}")
        
        print('사용되지 않는 재질을 삭제했습니다.')
        # cmds.confirmDialog(title='완료', message='사용되지 않는 재질을 삭제했습니다.', button=['OK'])
    
    def execute_checking_validation(self):
        
        pass
    
    def check_shadow_quality(self):
        lights = cmds.ls(type="light")
        for light in lights:
            if cmds.objExists(f"{light}.useRayTraceShadows"):
                ray_trace = cmds.getAttr(f"{light}.useRayTraceShadows")
                if ray_trace:
                    print(f"Light: {light} has raytrace shadows enabled.")
                    return True
                else:
                    print(f"Light: {light} does not have raytrace shadows enabled.")
                    return False
    def clean_animation_curves(self):
        anim_curves = cmds.ls(type="animCurve")
        
        for curve in anim_curves:
            cmds.filterCurve(curve)  # 커브를 정리하여 불필요한 키프레임 제거
            cmds.keyframe(curve, edit=True, removeZero=True)  # 값이 0인 키프레임 제거

        print("Animation curves cleaned.")
    
    def check_floating(character):
        contacts = ["foot_L", "foot_R"]  # 발의 컨트롤러 이름을 예로 들었습니다.
        floating_issues = []

        for contact in contacts:
            if cmds.objExists(contact):
                y_pos = cmds.getAttr(f"{contact}.translateY")
                if y_pos > 0.001:  # 바닥에서 너무 멀리 떨어져 있는지 체크
                    floating_issues.append(f"{contact} is floating: Y = {y_pos}")

        if floating_issues:
            print("Floating issues found:")
            for issue in floating_issues:
                print(issue)
        else:
            print("No floating issues detected.")
            
            

class ValidateByTask(ValidationCheckForMaya):
    print("_____________________ValidateByTask__________________")
    def __init__(self) -> None:
        super().__init__()
        
    def check_validation_list_for_task(self,task):
        check_list = [""]
        if task == "mod":
            check_list = ["Check if there are ngons or tri-polygons in the mesh. ","Check if there are any unused materials.","Check if there is no naming space."]
            
        elif task == "rig":
            check_list = ["Check if there are any unused materials.","Check if there is no naming space.","Check that parent chain and hierarchy are correct"]
        elif task == "lkd":
            check_list = ["Check if the texture resolution is appropriate.","Check if optimization for rendering time is appropriate.","Check whether shader properties are set correctly according to Physically Based Rendering (PBR) standards"]
        elif task == "mm":
            
            check_list = ["Check the RMS error value (Root Mean Square error) and review whether tracking was performed within the error range below a appropriate level.",
                          "Check whether the coordinate system set in the 3D software matches the matchmove data.",
                          "Make sure your matchmove data is saved in the correct format and that the file is not corrupted"]
            # return check_list
        elif task == "ani":
            check_list = ["Check whether contact points such as feet or hands naturally contact the ground or other objects.","Check whether joints such as elbows, knees, etc. are abnormally deformed"]
        elif task == "lgt":
            check_list = ["Global Illumination (GI) settings: Ensure GI is set correctly","Ambient Occlusion (AO) settings: Ensure AO is applied appropriately"]
            
            
        return check_list
    def validate_mod(self):
        self.check_all_non_quads()
        self.list_unused_materials()
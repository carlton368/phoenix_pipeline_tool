
from Publisher.Maya.maya_playblast_scene_setter import PlayblastSceneSetter
import maya.cmds as cmds
# 마야에서 퍼블리시 할 때 필요한 정보들을 관리하는 모듈
# 기능별로 클래스 구분함.
#[주요기능]
# 1. 아웃라이너 오브젝트 조사 
# 2. abc,shader,shader_json,mb 파일 저장
import os
import subprocess
import datetime
import maya.mel as mel
class MayaOutlinerInfoCatcher():
    """
    마야의 아웃라이너에 있는 오브젝트들의 이름을 ui에 띄우기 위해 
    조사하고, 간결화하는 클래스
    """
    def __init__(self, exclude_views=None):
        if exclude_views is None:
            exclude_views = ['persp', 'top', 'front', 'side']
        self.exclude_views = exclude_views

    def get_all_objects(self):
        """Maya 씬에서 모든 객체를 가져옵니다."""
        return cmds.ls(assemblies=True)
        
    def filter_objects(self,objects):
        """카메라와 제외할 뷰포트를 필터링합니다."""
        objs = []

        for obj in objects:
            if not obj in self.exclude_views:
                objs.append(obj)
            from importlib import reload
        return objs



    def simplify_object_name(self, name):
        """객체 경로에서 마지막 부분만 추출하여 단순화합니다."""
        if 'Shape' in name:
            return None
        return name.rpartition('|')[-1]

    def get_filtered_and_simplified_objects(self):
        """필터링과 단순화를 적용한 객체 리스트를 반환합니다."""
        all_objects = self.get_all_objects()
        filtered_objects = self.filter_objects(all_objects)
        
        print(filtered_objects)
        return filtered_objects
    
    def warn_file_path_messsage(self):
        cmds.confirmDialog(
                title='Warning!',
                message="There's no file path",
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel'
                    )
        
    def get_render_resolution(self):
        # 렌더 설정 노드가 존재하는지 확인
        render_settings_nodes = cmds.ls(type='renderSettings')
        
        if not render_settings_nodes:
            # 기본 렌더 설정 노드를 사용
            render_settings = 'defaultResolution'
        else:
            render_settings = render_settings_nodes[0]
        
        # 해상도 정보 가져오기
        resolution_width = cmds.getAttr(f"{render_settings}.width")
        resolution_height = cmds.getAttr(f"{render_settings}.height")
        
        return str(resolution_width), str(resolution_height)
    
    def list_used_materials(self, default_materials=None):    # 씬에서 사용되지 않는 재질을 리스트로 반환
        """
        씬에서 사용되지 않는 재질을 리스트로 반환합니다.
        
        :param default_materials: 기본 재질 목록. 삭제하지 않을 재질들을 포함합니다.
        :return: 사용되지 않는 재질의 리스트
        """
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
        return materials


    def get_all_layers(self):
        all_layers = cmds.ls(type="renderLayer")
        print(all_layers)
        return all_layers
    
    def get_list_used_materials(self, default_materials=None):    # 씬에서 사용되지 않는 재질을 리스트로 반환
        """
        씬에서 사용되는 재질을 리스트로 반환합니다.
        
        :param default_materials: 기본 재질 목록. 삭제하지 않을 재질들을 포함합니다.
        :return: 사용되지 않는 재질의 리스트
        """
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
        return all_materials
class MayaFileSaver(): 
    
    def save_selected_items_as_mb(self, selected_text_items, file_path):
        #선택된 오브젝트를 제외한 모든 정보들을 제거함
        # 새 신을 만들고, 카피함.
        all_objects = cmds.ls(assemblies = True )

        # 유효한 오브젝트들을 저장할 리스트
        valid_items = []
        
        for item in selected_text_items:
            # 각 오브젝트 이름이 DAG 경로의 일부일 수 있으므로, 전체 경로에서 일치 항목을 찾습니다.
            if item in all_objects:
                valid_items.append(item)
                if not valid_items:
                    print("선택된 유효한 오브젝트가 없습니다. 작업을 종료합니다.")
                    return None
            
        # 선택된 오브젝트들을 새로 선택합니다.
        cmds.select(valid_items, replace=True)
        print(f"유효한 오브젝트가 선택되었습니다: {valid_items}")
        
        # 선택되지 않은 모든 오브젝트를 제거합니다.
        all_objects = cmds.ls(assemblies = True)
        objects_to_delete = [obj for obj in all_objects if obj not in valid_items]
        
        if objects_to_delete:
            cmds.delete(objects_to_delete)
            print(f"선택되지 않은 오브젝트가 제거되었습니다: {objects_to_delete}")
        else:
            print("제거할 오브젝트가 없습니다.")
        
        # 파일 경로가 절대 경로인지 확인합니다. 절대 경로가 아니면 기본 작업 디렉토리와 결합합니다.
        if not os.path.isabs(file_path):
            directory = cmds.workspace(query=True, rootDirectory=True)
            file_path = os.path.join(directory, file_path)

        # 디렉토리가 존재하지 않으면 생성합니다.
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # MB 파일로 저장합니다.
        try:
            cmds.file(rename=file_path)
            cmds.file(save=True, type='mayaBinary')
            print(f"MB 파일이 {file_path}에 저장되었습니다.")
        except RuntimeError as e:
            print(f"파일 저장에 실패했습니다. 오류: {e}")
    
    def export_selected_items_as_alembic_and_mb(self, selected_text_items, new_version_dir,pub_path):
        """
        선택된 오브젝트들만 Alembic 파일과 Maya Binary 파일로 저장합니다.
        나머지 오브젝트는 제거합니다.

        :param selected_text_items: 선택된 오브젝트의 이름 목록
        :param export_abc_file_dir: Alembic 파일이 저장될 디렉토리 경로
        :param mb_file_path: Maya Binary 파일이 저장될 경로
        """

        print("newversion_dir",new_version_dir)
        all_objects = cmds.ls(assemblies = True)

        # 유효한 오브젝트들을 저장할 리스트
        valid_items = []
        
        for item in selected_text_items:
            if item in all_objects:
                valid_items.append(item)
                if not valid_items:
                    print("선택된 유효한 오브젝트가 없습니다. 작업을 종료합니다.")
                    return None
        if not valid_items:
            print("선택된 유효한 오브젝트가 없습니다. 작업을 종료합니다.")
            return

        # 선택된 오브젝트들을 새로 선택합니다.
        cmds.select(valid_items, replace=True)
        print(f"유효한 오브젝트가 선택되었습니다: {valid_items}")

        # 선택되지 않은 모든 오브젝트를 제거합니다.
        objects_to_delete = [obj for obj in all_objects if obj not in valid_items]

        if objects_to_delete:
            cmds.delete(objects_to_delete)
            print(f"선택되지 않은 오브젝트가 제거되었습니다: {objects_to_delete}")
        else:
            print("제거할 오브젝트가 없습니다.")

        # Alembic 내보내기
        start_frame = int(cmds.playbackOptions(query=True, min=True)) - 10
        end_frame = int(cmds.playbackOptions(query=True, max=True)) + 10
        
        #샷그리드에 올라갈 알렘빅 경로 리스트 
        abc_cache_paths = []
        
        
        
        for vaild_item in valid_items:
            # Alembic 파일 경로를 설정합니다.
            file_basename = os.path.basename(vaild_item) ###
            
            abc_path = f"{new_version_dir}/{file_basename}.abc" #변수 네이밍..
            print(abc_path)
            abc_cache_paths.append(abc_path)
            # Alembic 내보내기 옵션을 설정합니다.
            alembic_args = [
                "-renderableOnly",
                "-writeFaceSets",
                "-uvWrite",
                "-worldSpace",
                "-eulerFilter",
                f"-fr {start_frame} {end_frame}",
                f"-file '{abc_path}'",
                f"-root {vaild_item}"
            ]
            
            # Alembic 내보내기 명령을 실행합니다.
            abc_export_cmd = 'AbcExport -j "%s"' % " ".join(alembic_args)

            try:
                # Alembic 파일 디렉토리가 존재하지 않으면 생성합니다.
                if not os.path.exists(new_version_dir):
                    os.makedirs(new_version_dir)

                mel.eval(abc_export_cmd)
                print(f"Alembic 파일이 성공적으로 저장되었습니다: {abc_path}")
            except RuntimeError as e:
                    print(f"Alembic 내보내기에 실패했습니다. 오류: {e}")
        # Maya Binary 파일로 저장하기
        
        # 파일 경로가 절대 경로인지 확인합니다. 절대 경로가 아니면 기본 작업 디렉토리와 결합합니다.
        mb_file_path = f"{new_version_dir}/{file_basename}" #경로는 알렘빅이랑 똑같이 되서, 이미 확인됨,.
        
        

        try:
            cmds.file(rename=mb_file_path)
            cmds.file(save=True, type='mayaBinary')
            print(f"MB 파일이 {mb_file_path}에 저장되었습니다.") #필요한거>> END_001_v001 파일의 base 네임..
            
            
        except RuntimeError as e:
            print(f"MB 파일 저장에 실패했습니다. 오류: {e}")
            
            
        return abc_cache_paths, mb_file_path
    

    def render_exr(self,new_version_dir, pub_path, aovs, selected_layers):
        """
        씬의 카메라로 EXR 포맷으로 렌더링을 수행하는 함수입니다.
        Parameters:
        - new_version_dir (str): 렌더링된 파일을 저장할 디렉토리 경로입니다.
        - pub_path (str): 출력 파일의 기본 경로를 포함하는 파일 경로입니다.
        - aovs (list): 렌더링할 AOV의 목록입니다.
        """
        #################################################################################################
        #렌더링 경로 설정
        
        print("exr_렌더중...!")
        file_name = os.path.basename(pub_path)
        exr_dir = f"{new_version_dir}/exr/"
        exr_path = f"{exr_dir}.####.exr"
        deep_exr_dir = f"{exr_dir}deep/"
        deep_exr_path = f"{deep_exr_dir}deep_####.exr"  # deep AOV 전용 경로
        # camera_name = 'render_camera'  # 사용할 카메라의 이름을 지
        #################################################################################################33
        # 1. 렌더링에 사용할 카메라 설정
        
        print(f"File Name: {file_name}")
        print(f"EXR Directory: {exr_dir}")
        print(f"EXR Path: {exr_path}")
        print(f"Deep EXR Directory: {deep_exr_dir}")
        print(f"Deep EXR Path: {deep_exr_path}")
        # print(f"Camera Name: {camera_name}")
        ##################################################################################################3
        #렌더링 옵션에서 파일 이름에 대한 문자열을 포맷팅 할수 있습니다.
        #Scene>_<RenderLayer> 로 지정을 하면
        #FCG_0030_light_v001_LayerName <-- 이름을 만들수 있습니다.
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix","<RenderLayer>/<Scene>_<RenderLayer>", type="string")
        cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)
        cmds.setAttr("defaultRenderGlobals.animation", 1)
        cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
        cmds.setAttr('defaultRenderGlobals.imageFormat', 51) # EXR 포맷 (51 = EXR)
        cmds.setAttr('defaultArnoldDriver.mergeAOVs', 1) # AOV 합치기 설정
        #여기까지 하면 FCG_0030_light_v001_LayerName.####.exr <-- 로 파일 이름을 만들수 있어요.
        #모든 렌더레이어 리스트에 담기
        #이 리스트를 ui에 노출시켜서 선택할수 있도록 할수 있을것 같아요
        ##########################################################################################################
        #선택한 노드들만 리스트로 만들어주었다면.
        ###########################################################################################################3
        if not os.path.exists(exr_dir):
            os.makedirs(exr_dir)
        if not os.path.exists(deep_exr_dir):
            os.makedirs(deep_exr_dir)
        # 5. AOV 리스트를 설정 (이미 설정된 AOV들이 있다고 가정)
        
        for aov in aovs:
            sanitized_aov = aov.replace(" ", "_")
            aov_node_name = f'aiAOV_{sanitized_aov}'

            if not cmds.objExists(aov_node_name):
                aov_node = cmds.createNode('aiAOV', name=aov_node_name)
                cmds.setAttr(f'{aov_node}.name', sanitized_aov, type='string')
                
                
        # `deep` AOV를 별도로 렌더링
        if 'deep' in aovs:
            cmds.setAttr('defaultArnoldDriver.mergeAOVs', 0)  # AOV 병합 비활성화
            print("AOV merging disabled for deep AOV.")
            cmds.workspace(fileRule=['images', deep_exr_dir])
            print(f"Workspace path set to deep EXR path: {deep_exr_dir}")
            for selected_layer in selected_layers:
            # 렌더 레이어 변경하고,
                cmds.editRenderLayerGlobals(currentRenderLayer=selected_layer)
                # 렌더링 한다.
                cmds.arnoldRender(batch=True) #전체  프레임을 렌더링 함.
            print(f"Deep image rendered and saved to {deep_exr_dir}")
        # 렌더링: 모든 AOV를 합쳐서 기본 EXR 파일로 저장
        print(f"Workspace path set to: {exr_path}")
        for selected_layer in selected_layers:
            # 렌더 레이어 변경하고,
            cmds.editRenderLayerGlobals(currentRenderLayer=selected_layer)
            # 렌더링 한다.
            cmds.arnoldRender(batch=True) 
            #전체  프레임을 렌더링 함.
            
            cmds.workspace(fileRule=['images', exr_dir])
        print(f"Rendered image with merged AOVs saved to {exr_path}")
    
    
    def shader_collector(self):
       
        """
        룩뎁일경우에만
        셰이더와 오브젝트들을 컬렉션하는 함수.
        셰이더 딕셔너리..
        """
        shader_dictionary = {}
        shading_groups = cmds.ls(type="shadingEngine")
        for shading_group in shading_groups:
            shader = cmds.ls(cmds.listConnections(shading_group + ".surfaceShader"), materials=True)    
            if not shader:
                continue
            objects = cmds.sets(shading_group, q=True)
            shader_name = shader[0]
            if objects:
                if shader_name not in shader_dictionary:
                    shader_dictionary[shader_name] = []
                shader_dictionary[shader_name].extend(objects)
        return shader_dictionary
    
    def export_shader_ma_json(self,path):
        """
        maya에서 오브젝트에 어싸인된 셰이더들을 ma 파일로 익스포트하고,
        그 정보들을 json 파일로 익스포트 하는 함수이다.
        """
        import json
        import re
        pattern = r'v(\d{3})'
        match = re.search(pattern, path)
        version= match.group(0) #001 v떼고
        pub_dir = os.path.dirname(path)
        shader_dictionary = self.shader_collector()
        


        for shader, _ in shader_dictionary.items():
            cmds.select(shader, add=True)    

        ma_file_path = f"{pub_dir}/{version}/shader.ma"
        json_file_path = f"{pub_dir}/{version}/shader.json"
        print(ma_file_path)
        if not os.path.exists(f"{pub_dir}/{version}/"):
            os.makedirs(f"{pub_dir}/{version}/")
        
        cmds.file(ma_file_path, exportSelected=True, type="mayaAscii")
        
        with open(json_file_path, 'w') as f:
            json.dump(shader_dictionary, f)

        cmds.select(clear=True)
        return json_file_path, ma_file_path
    
    def asset_make_slate(self,path,project):
        """ 
        마야의 플레이 블라스트 기능을 이용해서 뷰포트를 이미지로 렌더링하고,
        슬레이트 정보를 삽입하여 동영상을 인코딩한다.
        image : jpg
        mov codec : h264
        """ 
        
        
        scene_setter = PlayblastSceneSetter()
        scene_setter.run_playblast_setup()
        
        pub_dir = os.path.dirname(path)
        pub_name = os.path.basename(path)
        proxy_path = f"{pub_dir}/.proxy"
        proxy_format = "jpg"
        image_path = os.path.join(proxy_path, 'proxy.%04d.' + proxy_format) #playblast에서 만든이미지 경로
        mov_path = f"{pub_dir}/.slate/slate.mov"
        
        if not os.path.exists(f"{pub_dir}/.slate"):
            os.makedirs(f"{pub_dir}/.slate")
        if not os.path.exists(f"{pub_dir}/.proxy"):
            os.makedirs(f"{pub_dir}/.proxy")
        
        start_frame = cmds.playbackOptions(query=True, min=True)
        last_frame = cmds.playbackOptions(query=True, max=True)
        render_width = 1920
        render_height = 1080
        
        cameras = cmds.ls(type='camera')
        print(cameras)
        for camera_ in cameras:
            if camera_ == "turntable_cameraShape1":
                cam_transform = cmds.listRelatives(camera_, parent=True)[0]
                print(f"Checking camera transform: {cam_transform}")
        model_panels = cmds.getPanel(type="modelPanel")
        if model_panels:
            for panel in model_panels:
                cmds.modelEditor(panel, e=True, displayLights="all")
                cmds.modelEditor(panel, e=True, shadows=True)
                cmds.modelEditor(panel, e=True, grid=False)
                print("조명과 그림자가 활성화 되었고 그리드는 비활성화 되었습니다.")

        cmds.lookThru(cam_transform)
        
        # PLAYBLAST MAYA API
        cmds.playblast(filename=os.path.join(proxy_path, 'proxy'), format='image', compression=proxy_format,
                    startTime=start_frame, endTime=last_frame, forceOverwrite=True,
                    widthHeight=(render_width, render_height), percent=100,
                    showOrnaments=True, framePadding=4, quality=100, viewer=False) #
        
        # FFMPEG 명령어 생성 및 실행
        first = 1
        frame_rate = 24 
        ffmpeg = "ffmpeg"
        slate_size = 60
        font_path = "/home/rapa/phoenix/phoenix_pipeline/maya/playblast/font/Courier Regular/Courier Regular.ttf"
        font_size = 40
        frame_count = last_frame - start_frame
        text_x_padding = 10
        text_y_padding = 20

        top_left = pub_name
        top_center = project
        top_right = datetime.date.today().strftime("%Y/%m/%d")
        bot_left = f"1920 X 1080"
        bot_center = ""        # split = file_basename.split(".")
        # abc = split[0]
        # abc_name = f"{abc}.abc" #abc 파일이름

        frame_cmd = "'Frame \: %{eif\:n+"
        frame_cmd += "%s\:d}' (%s)"  % (first, frame_count+1)
        bot_right = frame_cmd

        cmd = '%s -framerate %s -y -start_number %s ' % (ffmpeg, frame_rate, first)
        cmd += '-i %s' % (image_path)
        cmd += ' -vf "drawbox=y=0 :color=black :width=iw: height=%s :t=fill, ' % (slate_size)
        cmd += 'drawbox=y=ih-%s :color=black :width=iw: height=%s :t=fill, ' % (slate_size, slate_size)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=%s,' % (font_path, font_size, top_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=%s,' % (font_path, font_size, top_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=%s,' % (font_path, font_size, top_right, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=h-th-%s,' % (font_path, font_size, bot_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=h-th-%s,' % (font_path, font_size, bot_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=h-th-%s' % (font_path, font_size, bot_right, text_x_padding, text_y_padding)
        cmd += '"'
        cmd += ' -c:v prores_ks -profile:v 3 -colorspace bt709 %s' % mov_path
        
        subprocess.call(cmd, shell=True)
        
        return mov_path  # 동영상 경로를 반환
    
    def rig_make_slate(self,path,project):
        
        rig_playblast_scene_setter = PlayblastSceneSetter()
        rig_playblast_scene_setter.run_playblast_setup_for_rig()
        pub_dir = os.path.dirname(path)
        pub_name = os.path.basename(path)
        proxy_path = f"{pub_dir}/.proxy"
        proxy_format = "jpg"
        image_path = os.path.join(proxy_path, 'proxy.%04d.' + proxy_format) #playblast에서 만든이미지 경로
        mov_path = f"{pub_dir}/.slate/slate.mov"
        
        if not os.path.exists(f"{pub_dir}/.slate"):
            os.makedirs(f"{pub_dir}/.slate")
        if not os.path.exists(f"{pub_dir}/.proxy"):
            os.makedirs(f"{pub_dir}/.proxy")
        
        start_frame = cmds.playbackOptions(query=True, min=True)
        last_frame = cmds.playbackOptions(query=True, max=True)
        render_width = 1920
        render_height = 1080
        
        cameras = cmds.ls(type='camera')
        print(cameras)
        for camera_ in cameras:
            if camera_ == "turntable_cameraShape1":
                cam_transform = cmds.listRelatives(camera_, parent=True)[0]
                print(f"Checking camera transform: {cam_transform}")
        model_panels = cmds.getPanel(type="modelPanel")
        if model_panels:
            for panel in model_panels:
                cmds.modelEditor(panel, e=True, displayLights="all")
                cmds.modelEditor(panel, e=True, shadows=True)
                cmds.modelEditor(panel, e=True, grid=False)
                print("조명과 그림자가 활성화 되었고 그리드는 비활성화 되었습니다.")

        cmds.lookThru(cam_transform)
        
        # PLAYBLAST MAYA API
        cmds.playblast(filename=os.path.join(proxy_path, 'proxy'), format='image', compression=proxy_format,
                    startTime=start_frame, endTime=last_frame, forceOverwrite=True,
                    widthHeight=(render_width, render_height), percent=100,
                    showOrnaments=True, framePadding=4, quality=100, viewer=False) #
        
        # FFMPEG 명령어 생성 및 실행
        first = 1
        frame_rate = 24 
        ffmpeg = "ffmpeg"
        slate_size = 60
        font_path = "/home/rapa/phoenix/phoenix_pipeline/maya/playblast/font/Courier Regular/Courier Regular.ttf"
        font_size = 40
        frame_count = last_frame - start_frame
        text_x_padding = 10
        text_y_padding = 20

        top_left = pub_name
        top_center = project
        top_right = datetime.date.today().strftime("%Y/%m/%d")
        bot_left = f"1920 X 1080"
        bot_center = ""        # split = file_basename.split(".")
        # abc = split[0]
        # abc_name = f"{abc}.abc" #abc 파일이름

        frame_cmd = "'Frame \: %{eif\:n+"
        frame_cmd += "%s\:d}' (%s)"  % (first, frame_count+1)
        bot_right = frame_cmd

        cmd = '%s -framerate %s -y -start_number %s ' % (ffmpeg, frame_rate, first)
        cmd += '-i %s' % (image_path)
        cmd += ' -vf "drawbox=y=0 :color=black :width=iw: height=%s :t=fill, ' % (slate_size)
        cmd += 'drawbox=y=ih-%s :color=black :width=iw: height=%s :t=fill, ' % (slate_size, slate_size)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=%s,' % (font_path, font_size, top_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=%s,' % (font_path, font_size, top_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=%s,' % (font_path, font_size, top_right, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=h-th-%s,' % (font_path, font_size, bot_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=h-th-%s,' % (font_path, font_size, bot_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=h-th-%s' % (font_path, font_size, bot_right, text_x_padding, text_y_padding)
        cmd += '"'
        cmd += ' -c:v prores_ks -profile:v 3 -colorspace bt709 %s' % mov_path
        
        subprocess.call(cmd, shell=True)
        return mov_path 
        
    def shot_make_slate(self, path, project):
        """ 
        마야의 플레이 블라스트 기능을 이용해서 뷰포트를 이미지로 렌더링하고,
        슬레이트 정보를 삽입하여 동영상을 인코딩한다.
        image : jpg
        mov codec : h264
        """ 
        
        
        print("Starting shot_make_playblast...")
        print(f"Path: {path}")
        print(f"Project: {project}")

        pub_dir = os.path.dirname(path)
        shot_number = os.path.basename(path)
        shot = shot_number.split(".")[0]
        proxy_path = f"{pub_dir}/.proxy"
        proxy_format = "jpg"
        image_path = os.path.join(proxy_path, 'proxy.%04d.' + proxy_format)  # playblast에서 만든 이미지 경로
        mov_path = f"{pub_dir}/.slate/slate.mov"

        print(f"Proxy path: {proxy_path}")
        print(f"Image path: {image_path}")
        print(f"Movie path: {mov_path}")

        if not os.path.exists(f"{pub_dir}/.slate"):
            os.makedirs(f"{pub_dir}/.slate")
            print(f"Created directory: {pub_dir}/.slate")
        if not os.path.exists(f"{pub_dir}/.proxy"):
            os.makedirs(f"{pub_dir}/.proxy")
            print(f"Created directory: {pub_dir}/.proxy")
            
        start_frame = cmds.playbackOptions(query=True, min=True)
        last_frame = cmds.playbackOptions(query=True, max=True)
        print(f"Start frame: {start_frame}, Last frame: {last_frame}")

        render_width = 1920
        render_height = 1080
        
        cameras = cmds.ls(type='camera')
        print(cameras)
        for camera_ in cameras:
            if camera_ == "matchmove_cameraShape":
                cam_transform = cmds.listRelatives(camera_, parent=True)[0]
                print(f"Checking camera transform: {cam_transform}")
            elif camera_ == "anim_cameraShape":
                cam_transform = cmds.listRelatives(camera_, parent=True)[0]
                print(f"Checking camera transform: {cam_transform}")
                    
            
        
        
        cmds.lookThru(cam_transform)
        print(f"Set view through camera: {cam_transform}")

        # PLAYBLAST MAYA API
        cmds.playblast(filename=os.path.join(proxy_path, 'proxy'), format='image', compression=proxy_format,
                    startTime=start_frame, endTime=last_frame, forceOverwrite=True,
                    widthHeight=(render_width, render_height), percent=100,
                    showOrnaments=True, framePadding=4, quality=100, viewer=False)
        
        
        print("Playblast complete")

        # FFMPEG 명령어 생성 및 실행
        first = start_frame
        frame_rate = 24
        ffmpeg = "ffmpeg"
        slate_size = 60
        font_path = "/home/rapa/phoenix/phoenix_pipeline/maya/playblast/font/Courier Regular/Courier Regular.ttf"
        font_size = 40
        frame_count = last_frame - start_frame
        text_x_padding = 10
        text_y_padding = 20

        top_left = shot
        top_center = project
        top_right = datetime.date.today().strftime("%Y/%m/%d")
        bot_left = "1920x1080"
        bot_center = ""

        frame_cmd = "'Frame \: %{eif\:n+"
        frame_cmd += "%s\:d}' (%s)" % (first, frame_count + 1)
        bot_right = frame_cmd

        cmd = '%s -framerate %s -y -start_number %s ' % (ffmpeg, frame_rate, first)
        cmd += '-i %s' % (image_path)
        cmd += ' -vf "drawbox=y=0 :color=black :width=iw: height=%s :t=fill, ' % (slate_size)
        cmd += 'drawbox=y=ih-%s :color=black :width=iw: height=%s :t=fill, ' % (slate_size, slate_size)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=%s,' % (font_path, font_size, top_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=%s,' % (font_path, font_size, top_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=%s,' % (font_path, font_size, top_right, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=%s :y=h-th-%s,' % (font_path, font_size, bot_left, text_x_padding, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=(w-text_w)/2 :y=h-th-%s,' % (font_path, font_size, bot_center, text_y_padding)
        cmd += 'drawtext=fontfile=%s :fontsize=%s :fontcolor=white@0.7 :text=%s :x=w-tw-%s :y=h-th-%s' % (font_path, font_size, bot_right, text_x_padding, text_y_padding)
        cmd += '"'
        cmd += ' -c:v prores_ks -profile:v 3 -colorspace bt709 %s' % mov_path

        print(f"Executing FFMPEG command: {cmd}")
        subprocess.call(cmd, shell=True)
        print("FFMPEG command execution complete")
        return mov_path
        

    def set_freeze(self):
        """
        마야에서 선택한 애셋의 트랜스폼 정보를 디폴트 옵션으로 초기화한다.
        """
        asset = cmds.ls(selection=True)
        cmds.makeIdentity(asset, apply=True, translate=True, rotate=True,
                        scale=True, normal=True)

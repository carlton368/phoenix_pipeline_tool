import maya.cmds as cmds
import maya.mel as mel
from shotgun_api3 import Shotgun
from DataExploreForSceneSetting import DataExploreForSceneSetting
import re
import os
import sys

class LoaderSceneSetting:
    """
    Loader에서 Maya 파일을 열었을 때 Scene에 필요한 요소들을 셋팅해주는 클래스입니다.
    """
    # def __init__(self):
    #     self.data_explore = DataExploreForSceneSetting()
    #     self.dispatch_task()
    def __init__(self):
        self.data_explore = DataExploreForSceneSetting()
        self.load_alembic_plugin()
        self.dispatch_task()

    def load_alembic_plugin(self):
        plugins = ['AbcImport', 'AbcExport']
        for plugin in plugins:
            try:
                if not cmds.pluginInfo(plugin, query=True, loaded=True):
                    cmds.loadPlugin(plugin)
                print(f"{plugin} plugin loaded successfully")
            except Exception as e:
                print(f"Error loading {plugin} plugin: {e}")
                cmds.warning(f"Failed to load {plugin} plugin. Please check your Maya installation.")        
            
    def dispatch_task(self):    # Task별로 다른 씬 셋팅을 실행합니다.
        path_info = self.data_explore.extract_path_info()
        print(path_info)
        task = path_info['task_name']
        
        # Asset 파트 셋팅
        if task == 'mod':
            print('Modeling 씬 셋팅중')
            self.setup_frame_range()
            
        elif task == 'lkd':
            print('LookDev 씬 셋팅중')
            self.setup_frame_range()
            
        elif task == 'rig':
            print('Rigging 씬 셋팅중')
            self.setup_frame_range()
        
        # Shot    
        # 샷 정보의 frame range를 프레임 셋팅 해줘야함(sg_cut_in, sg_cut_out)
        elif task == 'ani':
            print('Animation 씬 셋팅중')
            self.setup_mm_undistortion_size()
            self.setup_mm_camera()
            
        elif task == 'lgt':
            print('Lighting 씬 셋팅중')
            self.setup_mm_undistortion_size()
            
        elif task == 'cmp':
            print('Compositing 씬 셋팅중')
            self.setup_mm_undistortion_size()
            
        elif task == 'mm':
            print('Matchmove 씬 셋팅중')
            self.setup_mm_undistortion_size()
    
    ###########################################################################################################
    """
    For Assets
    """
    def setup_frame_range(self): # 에셋 파트 프레임 셋팅(1001 - 1200)
        cmds.playbackOptions(minTime=1001, maxTime=1200, animationStartTime=1001, animationEndTime=1200)
        
    """
    For Shots
    """
    def setup_mm_undistortion_size(self):   # 마야 렌더 설정에 언디스토션 사이즈 넣어주기
        """
        Maya에서 매치무브 언디스토션을 위한 장면을 설정합니다.

        :param width: 해상도의 가로 픽셀 수 (기본값: 1920)
        :param height: 해상도의 세로 픽셀 수 (기본값: 1080)
        """
        
        mm_dic = self.data_explore.get_undistortion_dimensions()
        width = int(mm_dic['width'])
        height = int(mm_dic['height'])
        
        # 렌더 해상도 설정
        cmds.setAttr("defaultResolution.width", width)
        cmds.setAttr("defaultResolution.height", height)
        cmds.setAttr("defaultResolution.deviceAspectRatio", width / height)

        print(f"Scene setup complete for matchmove undistortion at {width}x{height} resolution.")
    
    # def setup_mm_camera(self):   # 매치무브 카메라 불러오기
    #     abc_path = self.data_explore.get_mm_alembic_cache()
    #     print(abc_path)
    #     if os.path.exists(abc_path):
    #         # mel_command = f'AbcImport -mode import "{abc_path}";'
    #         # mel.eval(mel_command)
    #         # print(f"Successfully imported Alembic file: {abc_path}")z
    #         cmds.AbcImport(abc_path, mode='import')
    #         print('abc importing...')
    #         # cmds.importFile(abc_path, type="Alembic")
    #     else:
    #         print(f"File does not exist: {abc_path}")
    def setup_mm_camera(self):
        abc_path = self.data_explore.get_mm_alembic_cache()
        print(f"Attempting to import Alembic file: {abc_path}")
        if os.path.exists(abc_path):
            try:
                # Python API를 사용한 import 시도
                cmds.file(abc_path, i=True, type="Alembic", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, namespace=":", options="v=0;", pr=True)
                print(f"Successfully imported Alembic file: {abc_path}")
            except Exception as e:
                print(f"Error importing Alembic file using Python API: {e}")
                try:
                    # MEL 명령어를 사용한 import 시도
                    mel.eval(f'file -import -type "Alembic" -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace ":" -options "v=0;" -pr "{abc_path}";')
                    print(f"Successfully imported Alembic file using MEL: {abc_path}")
                except Exception as e:
                    print(f"Error importing Alembic file using MEL: {e}")
                    cmds.warning(f"Failed to import Alembic file: {abc_path}")
        else:
            print(f"Alembic file does not exist: {abc_path}")
            cmds.warning(f"Alembic file not found: {abc_path}")
    
if __name__ == "__main__":
    test = LoaderSceneSetting(sys.argv)
    test.setup_mm_undistortion_size()
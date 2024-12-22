print("menu_실행됨")

import os
import sys
from importlib import reload
import maya.cmds as cmds
import maya.mel as mel

home_dir = os.path.expanduser('~')
script_dir = f'{home_dir}/_phoenix_'

sys.path.append(script_dir)
sys.path.append(f'{script_dir}/Saver/Maya')
sys.path.append(f"{script_dir}/ui")

def show_saver_handlier():
    import SaverUIHandler
    import data_explorer_json
    import file_saver
    import get_maya_path
    
    reload(SaverUIHandler)
    reload(data_explorer_json)
    reload(file_saver)
    reload(get_maya_path)
    
    global win
    reload(SaverUIHandler)
    win = SaverUIHandler.SaverUIHandler()
    win.show()

def show_publish_handlier():
    from Publisher.Maya import publish_handler
    
    global window
    reload(publish_handler)
    window = publish_handler.PublishHandler()
    window.show()
    

import sys

sys.path.append("/home/rapa/_phoenix_/Launcher/Loader/LoaderSceneSetting")

def add_custom_menu():
    """
    마야의 메인 윈도우에 메뉴를 추가하는 함수 입니다.
    lambda 함수는 함수의 실행을 허용하지 않고, 이벤트가 발생했을때 함수를 실행시킵니다.
    """
    
    gMainWindow = mel.eval('$window=$gMainWindow')
    custom_menu = cmds.menu(parent=gMainWindow, tearOff = True, label = 'pheonix') 
    cmds.menuItem(label="File save", parent=custom_menu, command=lambda *args: show_saver_handlier()
                  )
    cmds.menuItem(label="Publish..", parent=custom_menu, command= lambda *args : show_publish_handlier()
                  )
    maya_loader_scene_setting()
    
    
    
def maya_loader_scene_setting():
    from LoaderSceneSetting import LoaderSceneSetting
    from DataExploreForSceneSetting import DataExploreForSceneSetting
    from ShotgunReferenceUpdater import ShotgunReferenceUpdater

    print("해결될까?")
    test_scenesetting = LoaderSceneSetting()
    test_data = DataExploreForSceneSetting()
    print('겨울님의 씬레퍼런스 셋업')
    updater = ShotgunReferenceUpdater()
    updater.get_assets_latest_versions_and_update_references()

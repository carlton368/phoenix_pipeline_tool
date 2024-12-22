print("*" *30)
print("menu.py_09031817")
print("메뉴 스크립트가 실행됨")
print("*" *30)

import os
import sys
import nuke
from importlib import reload

home_dir = os.path.expanduser('~')
script_dir = f"{home_dir}/_phoenix_"

sys.path.append(script_dir)
sys.path.append(f"{script_dir}/Saver/Nuke")
sys.path.append(f"{script_dir}/ui")

def show_saver_handler():
    import SaverUIHandler
    import data_explorer_json
    import file_saver
    import get_nuke_path

    reload(SaverUIHandler)
    reload(data_explorer_json)
    reload(file_saver)
    reload(get_nuke_path)
    
    global win
    win = SaverUIHandler.SaverUIHandler()
    win.show()
    
menu_bar = nuke.menu("Nuke")
pheonix_menu = menu_bar.addMenu("phoenix")
pheonix_menu.addCommand("File save", show_saver_handler)

sys.path.append(f"{script_dir}/Publisher/Nuke")

def show_publish_handler():
    # # script_dir = "/home/rapa/_phoenix_/env/nuke/dev/python"
    # if script_dir not in sys.path:
    #     # sys.path.append(script_dir)
    # # reload(SaverUIHandler)
    
    script_dir = f"/home/rapa/_phoenix_/env/nuke/dev/python"
    if script_dir not in sys.path:
        sys.path.append(script_dir)
    import nuke_publish_handler
    # import FileSaver
    # import DataExplorerJson
    # import NukeCurrentPathImporter
    # reload(FileSaver)
    # reload(DataExplorerJson)
    # reload(NukeCurrentPathImporter)
    
    global win
    win = nuke_publish_handler.PublishHandler()
    win.show()
    
pheonix_menu.addCommand("File Publish", show_publish_handler)

# sys.path.append("/home/rapa/_phoenix_/Launcher/Loader/LoaderSceneSettingNuke")
# from nk_validator_advanced import NukeValidator

# validator = NukeValidator()
# validator.setup_scene()
# print("짜잔Initial scene setting completed1.")
# def initial_scene_setting():
#     validator.setup_scene()

# initial_setting_done = False

# def onCreateCallback():
#     global initial_setting_done
#     if not initial_setting_done:
#         initial_scene_setting()
#         initial_setting_done = True
#         print("짜잔Initial scene setting completed2.")
#     else:
#         print("이런Initial scene setting already done. Skipping.")

# # Nuke의 onCreate 콜백에 함수 등록
# nuke.addOnCreate(onCreateCallback)
# print("짜잔Initial scene setting completed3.")

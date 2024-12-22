"""
이 스크립트에는 뉴크 실행시 사전에 설정해야하는
스크립트나 플러그인, 기즈모들을 참조하는 스크립트가 작성되면 좋아요.
"""

print("*" *30)
print("init.py")
print("이니셜라이즈 스크립트가 실행됨09041052")
print("*" *30)

import nuke
import sys
sys.path.append("/home/rapa/_phoenix_/env/nuke/dev/python")

nuke.pluginAddPath("./gizmo")
nuke.pluginAddPath("./icons")
nuke.pluginAddPath("./lib/python3.9/site-packages")
nuke.pluginAddPath("/home/rapa/_phoenix_/env/nuke/dev/lib/python3.9/site-packages")

nuke.pluginAddPath("./lut")
nuke.pluginAddPath("./plugins")
nuke.pluginAddPath("./python")




nuke.pluginAddPath("./lib/python3.9")


####################씬쎼팅################################################################
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


import nuke
import sys
import os
import re

user_home = os.path.expanduser("~")
sys.path.append(f'{user_home}/_phoenix_/Launcher/Loader/LoaderSceneSettingNuke')
from nk_validator_advanced import NukeValidator

def extract_version_from_path(path): 
    """ 경로에서 version 정보를 반환한다. """ 
    version_matches = re.findall('_v(\d+)', path.replace("\\","/")) 
    if len(version_matches) < 1: 
        return -1
    return version_matches[-1]

def run_initial_setup():
    validator = NukeValidator()
    path = validator.get_file_path()
    print(f"파일 경로: {path}")
    version=extract_version_from_path(path)
    print(f"추출된 버전: {version}")
    if version == '001':
        validator.initial_setup_scene()
        print('최초 신세팅 성공')
    else:
        print('버전이 001이 아니므로 신세팅을 생략합니다.')
nuke.addOnScriptLoad(run_initial_setup)

import sys
sys.path.append("/home/rapa/_phoenix_/")
from importlib import reload
print("menu_실행됨")

from Saver.Maya import SaverUIHandler
from Publisher.Maya import publish_handler

def show_publish_handlier():
    global window
    reload(publish_handler)
    window = publish_handler.PublishHandler()
    window.show()
    
def show_saver_handlier():
    global window
    reload(SaverUIHandler)
    window = SaverUIHandler.SaverUIHandler()
    window.show()


def add_custom_menu():
    """
    마야의 메인 윈도우에 메뉴를 추가하는 함수 입니다.
    lambda 함수는 함수의 실행을 허용하지 않고, 이벤트가 발생했을때 함수를 실행시킵니다.
    """
    import maya.cmds as cmds
    import maya.mel as mel
    
    gMainWindow = mel.eval('$window=$gMainWindow')
    custom_menu = cmds.menu(parent=gMainWindow, tearOff = True, label = 'pheonix') 
    cmds.menuItem(label="File save", parent=custom_menu, command=lambda *args: show_saver_handlier()
                  )
    cmds.menuItem(label="Publish..", parent=custom_menu, command= lambda *args : show_publish_handlier()
                  )

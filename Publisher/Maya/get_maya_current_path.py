import maya.cmds as cmds

class MayaCurrentPathImporter():
    def show_file_path(*args):
        import maya.cmds as cmds
        
        # 현재 열려있는 파일의 경로를 가져옵니다.
        current_file = cmds.file(q=True, sceneName=True)
        print(current_file)
        
        return current_file
    
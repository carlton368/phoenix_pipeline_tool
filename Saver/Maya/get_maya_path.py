import maya.cmds as cmds  

class MayaCurrentPathImporter():
    def show_file_path(*args):
        script_path = None
        try:
            script_path = cmds.file(q=True, sn=True)
        except:
            print("파일이 저장되지 않았습니다.")
        
        return script_path
    

        
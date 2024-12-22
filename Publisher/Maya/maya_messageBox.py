
import maya.cmds as cmds

class MayaMessageBoxPrompter():
    def show_version_not_saved_warning(self):
        
        print("msg_실행됨")
        cmds.confirmDialog(
            title='Warning',
            message='You should save your file first.',
            button=['OK'],
            icon='warning'
        )


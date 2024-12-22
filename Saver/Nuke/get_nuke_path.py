class NukeCurrentPathImporter():
    def show_file_path(*args):
        import nuke
        script_path = None
        try:
            script_path = nuke.scriptName()
        except:
            print("파일이 저장되지 않았습니다.")
        
        return script_path
    

        
import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel
from PySide6.QtCore import QFile, Signal, QTimer
from PySide6.QtUiTools import QUiLoader
from shotgun_api3 import Shotgun
from Launcher.Login.ui_login import Ui_Form


class Login(QWidget):
    login_success = Signal(str)  # 로그인 성공 시 이메일을 전달하는 시그널############################################변경사항: login_success 시그널 추가###############################################################
    def __init__(self, shotgun_client=None):##############변경사항: shotgun_client=None 추가###############################################################
        super().__init__()

        # UI 경로 설정 
        # ui_file_path = 'login.py'
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # self.ui = QUiLoader().load(ui_file, self)
        # ui_file.close()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Welcome Phoenix")

        # # 샷그리드 연결
        # script_name = "kimgyeoul"
        # script_key = "sBwdjezpc&zxhlyr5iqwbkgrn"
        # server_url = "https://4thacademy.shotgrid.autodesk.com/"
        # self.sg = Shotgun(server_url, script_name, script_key)

        # Shotgun 연결 설정 (위에 주석 처리한 부분 아래로 대체)################################################################################################################
        self.shotgun_client = shotgun_client
        if not self.shotgun_client:
            script_name = "kimgyeoul"
            script_key = "sBwdjezpc&zxhlyr5iqwbkgrn"
            server_url = "https://4thacademy.shotgrid.autodesk.com/"
            self.sg = Shotgun(server_url, script_name, script_key)
        else:
            self.sg = self.shotgun_client.shotgun_api_object()
        ############################################################################################################################################################################
        # UI 이벤트 연결############################################################################################################findchild 없이 직접 연결############################################################################################################
        self.email_input = self.ui.lineEdit
        self.login_button = self.ui.pushButton
        self.status_label = self.ui.label_3
        self.login_button.clicked.connect(self.on_login)
        
    # 로그인 함수
    def on_login(self):
        email = self.email_input.text()
        user = self.sg.find_one('HumanUser', [['email', 'is', email]], 
                                ['id', 'firstname', 'lastname', 'projects']) 
        
        if user:
            user_name = f"{user.get('firstname', '')} {user.get('lastname', '')}"
            self.status_label.setText(f'{user_name}님으로 로그인되었습니다.')     
 
            user_id = user['id']
            projects = self.sg.find('Project', [['users', 'is', 
                                    {'type': 'HumanUser', 'id': 
                                     user_id}]], ['id', 'name'])
            
            for project in projects:
                print(project['name'])  
                
            
            tasks = self.sg.find('Task', [['project', 'is', project], 
                                ['task_assignees', 'is', 
                                {'type': 'HumanUser', 'id': 
                                user_id}]], ['content','due_date', 'entity', 'id'])
            
            for task in tasks:
                print(task['content'], task['due_date'], task['entity'], task['id'])  
                
##################################################################################################################                
            self.login_success.emit(email)  # 로그인 성공 시그널 발생############################################변경사항: 로그인 성공 시 이메일을 전달하는 시그널 발생###############################################################
            # self.open_loader(email)  # 주석 처리
        else:
            self.status_label.setText('유저가 없습니다')

 
            
            ##########주석처리############################################################################################################
    # def open_loader(self, email):
    #     # 새로운 프로세스로 MainWindow 실행
    #     subprocess.Popen([sys.executable, './Loader/loader_main.py', email])
        
    #     # 현재 로그인 창 닫기
    #     # window.close()
    #     pass
        

################################################################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())




















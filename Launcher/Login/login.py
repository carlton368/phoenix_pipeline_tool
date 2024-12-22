import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel
from PySide6.QtCore import QFile, Signal, QTimer
from PySide6.QtUiTools import QUiLoader
from shotgun_api3 import Shotgun
from ui.ui_login import Ui_Form

class Login(QWidget):
    login_success = Signal(str)  # 로그인 성공 시 이메일을 전달하는 시그널############################################변경사항: login_success 시그널 추가###############################################################
    def __init__(self, shotgun_client=None):
        super().__init__()

        # UI 경로 설정 
        # ui_file_path = '/home/rapa/_phoenix_/ui/login.ui' # 본인 경로로 변경
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # self.ui = QUiLoader().load(ui_file, self)
        # ui_file.close()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 샷그리드 연결
        # script_name = "kimgyeoul"
        # script_key = "sBwdjezpc&zxhlyr5iqwbkgrn"
        # server_url = "https://4thacademy.shotgrid.autodesk.com/"
        # self.sg = Shotgun(server_url, script_name, script_key)
        self.shotgun_client = shotgun_client
        if not self.shotgun_client:
            script_name = "kimgyeoul"
            script_key = "sBwdjezpc&zxhlyr5iqwbkgrn"
            server_url = "https://4thacademy.shotgrid.autodesk.com/"
            self.sg = Shotgun(server_url, script_name, script_key)
        else:
            self.sg = self.shotgun_client.shotgun_api_object()
            
        # UI 이벤트 연결
        self.email_input = self.ui.lineEdit
        self.login_button = self.ui.pushButton     
        self.login_button.clicked.connect(self.on_login)
        self.email_input.returnPressed.connect(self.on_login)  # 이 줄을 추가합니다
        self.setWindowTitle("login")
        self.status_label = self.ui.label_3

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
        else:
            self.status_label.setText('유저가 없습니다')

 
            
            
    # def open_loader(self, email):
    #     # 새로운 프로세스로 MainWindow 실행
    #     subprocess.Popen([sys.executable, 'mainwindow_V34001.py', email])
        
    #     # 현재 로그인 창 닫기
    #     window.close()
        

################################################################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())




















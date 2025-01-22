import sys
from PySide6.QtWidgets import QApplication
from Launcher.Login.login import Login
from Launcher.Loader.loader_main import MainWindow
from core.shotgun_api_client import ShotGunAPIclient

class MainApplication:  # Main application class
    """메인 애플리케이션 클래스"""
    def __init__(self):
        self.app = QApplication(sys.argv)   #어플리케이션 생성
        self.shotgun_client = ShotGunAPIclient()    #ShotGunAPI client 객체 생성    
        self.login_window = None    #로그인 창
        self.loader_window = None   #로더 창

    def start_login(self):  #어플리케이션 실행 함수
        """애플리케이션 시작!, 로그인 창을 보여주고 Qt 이벤트 루프 시작"""
        self.show_login()   #로그인 창을 띄움
        return self.app.exec()  #어플리케이션 실행

    def show_login(self):   #로그인 창을 띄우는 함수
        """로그인 창을 생성하고 표시. 로그인 성공 시그널을 on_login_success 메서드에 연결합니다."""
        self.login_window = Login(self.shotgun_client)  #로그인 창 생성: Login 클래스 생성자에 ShotGunAPIclient 객체를 전달
        # login_success 시그널을 연결. 로그인이 성공하면 login_success 시그널이 발생하고, email을 on_login_success 메서드에 전달합니다(important)
        self.login_window.login_success.connect(self.on_login_success)  #로그인 성공 시 on_login_success 함수 실행
        self.login_window.show()    #로그인 창 띄우기

    def on_login_success(self, email):
        """로그인 성공 시 호출되는 메서드, 로그인 창을 닫고 로더 창을 표시"""
        print(f"LOGIN SUCCESS : WELCOME! {email}")  #로그인 성공 시 이메일 출력
        self.login_window.close()   #로그인 창 닫기
        self.show_loader(email) #로더 창 띄우기

    def show_loader(self, email):   #로더 창을 띄우는 함수
        """로더 창을 생성하고 표시, 이메일과 Shotgun 클라이언트를 전달"""
        self.loader_window = MainWindow(email=email, shotgun_client=self.shotgun_client)    #로더 창 생성
        self.loader_window.show()   #로더 창 띄우기
    
if __name__ == "__main__":
    """애플리케이션이 종료되면 시스템 종료 코드"""
    main_app = MainApplication()    #MainApplication 클래스 생성
    sys.exit(main_app.start_login())  #어플리케이션 실행

#!/usr/bin/env python3
# 이 스크립트가 Python 3 인터프리터로 실행되도록 설정

import sys  # 시스템 관련 기능(예: 명령줄 인자, 시스템 종료)을 사용하기 위해 import
import os  # 운영체제와 관련된 기능(파일 경로, 권한 등)을 사용하기 위해 import
from pathlib import Path  # 경로 관련 작업을 더 간단하게 수행하기 위해 import
from PySide6.QtWidgets import QApplication  # PySide6 라이브러리에서 GUI 애플리케이션을 생성하기 위해 import
from Launcher.Login.login import Login  # 커스텀 로그인 창 클래스를 사용하기 위해 import
from Launcher.Loader.loader_main import MainWindow  # 커스텀 메인 윈도우 클래스를 사용하기 위해 import
from core.shotgun_api_client import ShotGunAPIclient  # Shotgun API와의 통신을 위한 클라이언트를 사용하기 위해 import

def create_desktop_file(app_name, exec_path, icon_path=None):
    """
    Linux 환경에서 애플리케이션의 .desktop 파일을 생성하는 함수
    :param app_name: 애플리케이션 이름 (메뉴에 표시될 이름)
    :param exec_path: 애플리케이션 실행 파일의 경로
    :param icon_path: 애플리케이션 아이콘 파일의 경로 (선택 사항)
    """
    # .desktop 파일의 내용을 정의
    desktop_file_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Phoenix
Exec=/usr/bin/python3.9 /home/rapa/_phoenix_/phoenix_main.py
Terminal=false
Categories=Utility;Development;
Icon=/home/rapa/_phoenix_/ui/desktop_icon.png"""
    
    if icon_path:
        # 아이콘 경로가 제공되었으면 Icon 항목을 추가
        desktop_file_content += f"Icon={icon_path}\n"
    
    # .desktop 파일이 저장될 디렉토리 경로 설정 (사용자 홈 디렉토리 내)
    desktop_dir = Path.home() / ".local" / "share" / "applications"
    desktop_dir.mkdir(parents=True, exist_ok=True)  # 디렉토리가 없으면 생성
    
    # 애플리케이션 이름을 기반으로 .desktop 파일의 경로 설정
    desktop_file_path = desktop_dir / f"{app_name.lower().replace(' ', '-')}.desktop"
    
    # .desktop 파일을 생성하고 내용을 작성
    with open(desktop_file_path, "w") as f:
        f.write(desktop_file_content)
    
    # .desktop 파일에 실행 권한을 부여
    os.chmod(desktop_file_path, 0o755)
    
    # .desktop 파일이 생성된 경로를 출력
    print(f".desktop 파일이 다음 위치에 생성되었습니다: {desktop_file_path}")

class MainApplication:
    """메인 애플리케이션 클래스. 전체 애플리케이션의 실행을 관리"""
    
    def __init__(self):
        # QApplication 객체 생성, GUI 애플리케이션의 진입점
        self.app = QApplication(sys.argv)
        
        # ShotGunAPIclient 객체 생성, Shotgun API와의 상호작용을 위한 클라이언트
        self.shotgun_client = ShotGunAPIclient()
        
        # 로그인 창과 로더 창을 None으로 초기화
        self.login_window = None
        self.loader_window = None

    def start_login(self):
        """애플리케이션을 시작하고 로그인 창을 보여주는 함수"""
        self.show_login()  # 로그인 창 표시
        return self.app.exec()  # Qt 이벤트 루프 시작

    def show_login(self):
        """로그인 창을 생성하고 화면에 표시하는 함수"""
        # Login 객체 생성, Shotgun 클라이언트를 전달
        self.login_window = Login(self.shotgun_client)
        
        # 로그인 성공 시그널을 on_login_success 메서드에 연결
        self.login_window.login_success.connect(self.on_login_success)
        
        # 로그인 창을 화면에 표시
        self.login_window.show()

    def on_login_success(self, email):
        """로그인 성공 시 호출되는 함수. 로그인 창을 닫고 로더 창을 표시"""
        print(f"로그인 성공: {email}")  # 로그인 성공 메시지와 이메일 출력
        
        # 로그인 창을 닫음
        self.login_window.close()
        
        # 로더 창 표시
        self.show_loader(email)

    def show_loader(self, email):
        """로더 창을 생성하고 화면에 표시하는 함수"""
        # MainWindow 객체 생성, 이메일과 Shotgun 클라이언트를 전달
        self.loader_window = MainWindow(email=email, shotgun_client=self.shotgun_client)
        
        # 로더 창을 화면에 표시
        self.loader_window.show()

if __name__ == "__main__":
    """스크립트가 직접 실행될 때 실행되는 코드 블록"""
    
    # 시스템 플랫폼이 Linux인 경우에만 .desktop 파일 생성
    if sys.platform.startswith('linux'):
        app_name = "Phoenix"  # 애플리케이션 이름 설정
        user_home_path = os.path.expanduser('~')
        exec_path = f"{user_home_path}/_phoenix_/phoenix_main.py"
        icon_path = f"{user_home_path}/_phoenix_/ui/desktop_icon.png"  # 아이콘 파일 경로 설정 (필요시 수정)
        
        # .desktop 파일 생성 함수 호출
        create_desktop_file(app_name, exec_path, icon_path)
    
    # MainApplication 클래스의 인스턴스 생성
    main_app = MainApplication()
    
    # 로그인 절차를 시작하고 애플리케이션 종료 시 반환 코드 전달
    sys.exit(main_app.start_login())

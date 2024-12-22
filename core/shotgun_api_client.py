from core.core_config_manager import ConfigManager
from typing import Tuple, Optional
import shotgun_api3

class ShotGunAPIclient:
    """
    싱글톤 디자인 패턴을 사용하여 인스턴스가 하나만 생성되도록 함. import한 shotgun_api3d의 Shotgun 클래스를 사용하여 Shotgun 서버와 통신
    sg는 shotgun_api3.Shotgun 클래스의 인스턴스로 한 번만 생성되며, 이후에 ShotGunAPIclient 클래스를 인스턴싱 시에도 동일한 객체를 반환
    """
    FALLBACK_URL = 'https://4thacademy.shotgrid.autodesk.com',
    FALLBACK_SCRIPT_NAME = 'wonjinLEE',
    FALLBACK_API_KEY = 'a7dHrocwtavnfoupawlmavw@n'

    _instance = None
    sg = None

    def __new__(cls):   # init 전에 호출되는 클래스 메소드! self가 아니라 cls를 인자로 받는다.
        """ <싱글톤 디자인 패턴> 클래스 자신의 인스턴스가 하나만 존재하도록 _instance가 None일 때만 인스턴스 생성"""
        if not cls._instance:   # 인스턴스가 없으면
            print("<ShotGunAPIclient> 최초 실행")   
            cls._instance = super().__new__(cls)    # 부모 클래스(object)의 __new__ 메소드 호출
            cls._instance.initialize_shotgun_api_client()  # Shotgun API 클라이언트 초기화
        return cls._instance

    def initialize_shotgun_api_client(self):   # Shotgun API 클라이언트 초기화 메서드
        print("<ShotGunAPIclient> 초기화 중...")
        self.instancing_modules_classes()   # 모듈의 클래스 인스턴스화
        if self.sg is None: # Shotgun API 객체가 생성되지 않았을 때
            shotgun_url, script_name, api_key = self.get_shotgun_config()
            self.create_shotgun_api_object(shotgun_url, script_name, api_key)   # Shotgun API 객체 생성

    def instancing_modules_classes(self):
        print("<ShotGunAPIclient> 사용할 모듈들의 클래스 인스턴스화 중...")
        self.config = ConfigManager()   # Create an instance of ConfigManager
        
    def get_shotgun_config(self) -> Tuple[str, str, str]:    # Shotgun 설정 가져오기 메서드
        print("<ShotGunAPIclient> Shotgun 설정 가져오기 중...")
        shotgun_url = self.config.get_value_as_str('Shotgun', 'shotgun_url')    # Shotgun URL 가져오기
        script_name = self.config.get_value_as_str('Shotgun', 'admin_script_name')  # 스크립트 이름 가져오기
        api_key = self.config.get_value_as_str('Shotgun', 'admin_api_key')  # API 키 가져오기
        return shotgun_url, script_name, api_key    # Shotgun URL, 스크립트 이름, API 키 반환

    def create_shotgun_api_object(self, shotgun_url: Optional[str] = None, script_name: Optional[str] = None, api_key: Optional[str] = None):   # Shotgun API 객체 생성 메서드
        """ Shotgun API 객체 생성 메서드"""
        try:
            self.sg = shotgun_api3.Shotgun(shotgun_url, script_name, api_key)   # Shotgun API 객체 생성
            print("<ShotGunAPIclient> Shotgun API 객체 생성 완료")
        except Exception as e:
            print(f"<ShotGunAPIclient> Shotgun API 객체 생성 실패: {e}")
            self.sg = None  # Shotgun API 객체 생성 실패 시 None으로 설정

    def emergency_shotgun_api_object_creation(self):   # 비상용 Shotgun API 객체 생성 메서드
        print("<ShotGunAPIclient> Shotgun API 객체 없음. 비상 키로 다시 생성 중...")
        try:
            self.sg = shotgun_api3.Shotgun(self.FALLBACK_URL,self.FALLBACK_SCRIPT_NAME,self.FALLBACK_API_KEY)
            return self.sg 
        except Exception as e:
            print(f"<ShotGunAPIclient> Shotgun API 객체 생성 실패: {e}")             
        print("<ShotGunAPIclient> Shotgun API 객체 생성 완료")

    def shotgun_api_object(self):   # Shotgun API 객체 반환 메서드
        return self.sg  # Shotgun API 객체 반환

    def is_shotgun_api_object_created(self, sg = None) -> bool:    # Shotgun API 객체 생성 여부 확인 메서드
        """ Shotgun API 객체 생성 여부 확인 메서드 """
        print("<ShotGunAPIclient> Shotgun API 객체 생성 여부 확인 중...")
        result = sg is not None    # Shotgun API 객체가 생성되었는지 확인, 생성되었으면 True
        return result   # 생성 여부 반환
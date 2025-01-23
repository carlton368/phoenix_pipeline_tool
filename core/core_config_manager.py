import os
import configparser 

class ConfigManager:
    """ loader_config.ini(설정 파일)을 관리 """ 
    _instance = None    # 싱글톤 패턴을 위한 클래스 변수(싱글톤 인스턴스를 저장하는 데 사용)
    base_path = None 
    cache_path = None
    user_home_path = os.path.expanduser('~')    # 사용자 홈 경로
    config_path = os.path.join(os.path.dirname(__file__), 'core_config.ini') # 설정 파일 경로
    
    def __new__(cls) -> 'ConfigManager':   # init 전에 호출되는 클래스 메소드! self가 아니라 cls를 인자로 받는다.
        """ <싱글톤 디자인 패턴> 클래스 자신의 인스턴스가 하나만 존재하도록 _instance가 None일 때만 인스턴스 생성"""
        if cls._instance is None:   # 인스턴스가 없으면
            cls._instance = super().__new__(cls) # 부모 클래스(object)의 __new__ 메소드 호출
            cls._instance._load_config()    # 설정 파일 로드
            cls._instance._set_base_path()   
            cls._instance._set_cache_path() 
        return cls._instance    # 인스턴스 반환
    
    def _load_config(self): 
        """ 'loader_config.ini'을 읽고 self.config에 저장 """
        self.config = configparser.ConfigParser()   # ConfigParser 객체 생성
        self.config.read(self.config_path)  # config 파일 읽기
        print(f"설정 파일 로드됨: {self.config_path}")
    
    def get_value_as_str(self, section: str, key: str, fallback = None): 
        """ 파라미터로 받은 섹션 이름, 키 이름을 바탕으로 config.ini에서 값을 가져온 후 실제 유저 홈 경로로 변환하여 반환"""
        raw_value = self.config.get(section, key, fallback=fallback) 
        converted_value = str(raw_value)
        result = converted_value.replace('{user_home}', os.path.expanduser('~'))
        return result
        
    def _set_base_path(self):   
        self.base_path = self.get_value_as_str('Paths', 'base_dir', fallback='')
        if not self.base_path:  
            self.base_path = os.path.join(self.user_home_path, 'phoenix_pipeline_tool')
        print(f'base_path : {self.base_path}')
    def _set_cache_path(self):
        self.cache_path = self.get_value_as_str('Paths', 'cache_dir', fallback='')
        print(f'self.cache_path는 {self.cache_path}')
        
    def get_base_path(self) -> str:
        return self.base_path 
    
    def get_cache_path(self) -> str:
        return self.cache_path
        
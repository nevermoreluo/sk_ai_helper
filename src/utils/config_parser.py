from configparser import ConfigParser

class SkConfig:
    def __init__(self, path: str):
        self.config = ConfigParser()
        self.config.read('config.ini')

    def get_int(self, section_name: str, option: str, default: int=0, **kw) -> int:
        if not self.config.has_section(section_name):
            return default
        if not self.config.has_option(section_name, option):
            return default
        return self.config.getint(section_name, option, **kw)

    def get_str(self, section_name: str, option: str, default: str="", **kw) -> str:
        if not self.config.has_section(section_name):
            return default
        if not self.config.has_option(section_name, option):
            return default
        return self.config.get(section_name, option, **kw)

    def get_bool(self, section_name: str, option: str, default: bool=False, **kw) -> bool:
        if not self.config.has_section(section_name):
            return default
        if not self.config.has_option(section_name, option):
            return default
        return self.config.getboolean(section_name, option, **kw)
    
    
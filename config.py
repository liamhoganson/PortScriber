from configparser import ConfigParser

class EnvConfig:
    def __init__(self):
        self.config_file: str = "config.ini"
        self.config = ConfigParser()

    def get_config(self, section: str, option: str) -> str:
        self.config.read(self.config_file)
        try:
            return self.config.get(section, option)
        except Exception:
            raise f"Could not find config value for {section}, {option}"

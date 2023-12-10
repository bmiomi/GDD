
from typing import Dict
from .FTP.config import ConfigFtp
from .Server.config import ConfigServer
from .Status.config import ConfigStatus


class ConfigFactory:
    @classmethod
    def getModulo(cls, value: Dict = None) -> object:

        config=value.get('Modulo')

        if config == "Server":
            return ConfigServer()
        if config == "FTP":
            return ConfigFtp()
        if config == "Status":
            return ConfigStatus()



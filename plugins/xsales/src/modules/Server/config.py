
from typing import Dict
from plugins.xsales.src.service.excelservice.service_excel import ExcelFile
from plugins.xsales.confi import Config
from plugins.xsales.util import sep

class ConfigServer(Config):
    """
    Configuración específica del módulo Server.
    Autocontenida - maneja sus propias credenciales y consultas.
    """

    spinner = 'bouncingBall'
    
    __credencialuser:str=''
    __credencialpassword:str=''

    @property
    def configserver(self)->Dict:
        return self.config.get('datod', {}).get('Server', {})
   
    @property
    def configConsultas(self)->Dict:
        return self.config.get('datod', {}).get('Server', {}).get('Consultas', {})

    @property
    def CredencialesServer(self):
        """
        Obtiene credenciales del servidor desde variables de entorno.
        Fallback a config.yml si no existe en .env
        """
        from core.config_manager import config_manager
        try:
            password, user = config_manager.get_server_default_credentials()
            self.__credencialuser = user
            self.__credencialpassword = password
            return (password, user)
        except ValueError:
            # Fallback a config.yml para migración gradual
            respuesta = self.configserver.get('credenciales', [{}])[0].get('default', {})
            if isinstance(respuesta, dict):
                self.__credencialuser = respuesta.get('USER', '')
                self.__credencialpassword = respuesta.get('PASSWORD', '')
            return (self.__credencialpassword, self.__credencialuser)
    
    @CredencialesServer.setter
    def CredencialesServer(self, credencial) -> None:
        """Setter de credenciales desde config.yml (legacy)"""
        credenciales = self.configserver.get('credenciales', [])
        for opcion in credenciales:
            if opcion.get(credencial):
                self.__credencialuser = opcion[credencial]['USER']
                self.__credencialpassword = opcion[credencial]['PASSWORD']
                return
        raise Exception(f'No se encontro credencial para {credencial} en el archivo config')
    
    @property
    def folderexcel(self) -> str:
        currpath = self.path.join(
            self.config.get('PathFolder').get('folder_file_excel'),
            self.fecha
        )

        if not self.path.isdir(currpath):
            self.nuevacarpeta(currpath)
        return currpath+sep
    
    @property
    def folderMadrugada(self) -> str:
        foldermadrugada = self.config.get('PathFolder').get('folderMadrugada')
        if not self.path.isdir(foldermadrugada):
            self.nuevacarpeta(foldermadrugada)
        return foldermadrugada+sep

    @property
    def excelfile(self):
        return ExcelFile


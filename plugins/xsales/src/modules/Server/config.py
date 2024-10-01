
from typing import Dict
from plugins.xsales.src.service.excelservice.service_excel import ExcelFile
from plugins.xsales.confi import Config
from plugins.xsales.util import sep

class ConfigServer(Config):

    spinner = 'bouncingBall'
    
    __credencialuser:str=''
    __credencialpassword:str=''

    @property
    def configserver(self)->Dict:
        return self.config.get('datod').get('Server')


    @property
    def CredencialesServer(self):
        respuesta=self.configserver.get('credenciales')[0].get('default')
        if isinstance(respuesta,dict):
            self.__credencialuser=respuesta['USER']
            self.__credencialpassword=respuesta['PASSWORD'] 
        return (self.__credencialpassword,self.__credencialuser)  
    
    @CredencialesServer.setter
    def CredencialesServer(self,credencial) -> None:
        credenciales = self.configserver.get('credenciales')
        for opcion in credenciales:
            if opcion.get(credencial):
                self.__credencialuser=opcion[credencial]['USER'], 
                self.__credencialpassword=opcion[credencial]['PASSWORD']
            else:
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


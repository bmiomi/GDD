
from typing import Dict
from plugins.xsales.src.service.excelservice.service_excel import ExcelFile
from plugins.xsales.confi import Config
from plugins.xsales.util import sep

class ConfigServer(Config):

    spinner = 'bouncingBall'
    
    __credencialuser:str=''
    __credencialpassword:str=''
    __credencialName:str='default'

    @property
    def configserver(self)->Dict:
        return self.config.get('datod').get('Server')
   
    @property
    def configConsultas(self)->Dict:
        return self.config.get('datod').get('Server').get('Consultas')

    @property
    def CredencialesServer(self):
        credencialname=self.__credencialName
        respuesta=self.buscar_credenciales(credencialname)
        if respuesta:
            self.__credencialuser=respuesta[self.__credencialName]['USER']
            self.__credencialpassword=respuesta[self.__credencialName]['PASSWORD'] 
        return (self.__credencialuser,self.__credencialpassword,)  
    
    @CredencialesServer.setter
    def CredencialesServer(self,credencial) -> None:
        self.__credencialName=credencial
        credenciales = self.buscar_credenciales(credencial)
        self.__credencialuser=credenciales[self.__credencialName]['USER'], 
        self.__credencialpassword=credenciales[self.__credencialName]['PASSWORD']

    @property
    def credencialuser(self):
        return self.__credencialuser

    @property
    def credencialpassword(self):
        return self.__credencialpassword


    def buscar_credenciales(self,credencial_name:str)->Dict:
        try:
            credencial = next(
                (credencial for credencial in self.configserver.get('credenciales')
                 if  credencial_name in credencial ),
                None
            )
            return credencial
        except KeyError:
            print("No se encontró la clave en el diccionario")
            return None


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


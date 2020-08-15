import argparse
from configparser import ConfigParser
from datetime import datetime
import os
#import errno

class configuracion:

    _path='.'+os.path.sep+'Distribuidores'

    def __init__(self):
        self._parser = argparse.ArgumentParser(description='seleciona la bandera del DZ  para validar el modulos de GDD')
        self.config=ConfigParser()
        self.__user=None
        self.__pass=None
        self.__ruta=None
        self.argumentos()
        self.credenciales()

    @property
    def USER(self):
        return self.__user

    @USER.setter
    def setterUSER(self,value):
        self.__user=value.replace("'",'')
        return self.__user

    @property   
    def PASS(self):
        return self.__pass

    @PASS.setter   
    def settPASS(self,value):
        self.__pass=value.replace("'",'')
        return self.__pass

    @property
    def FECHA(self):
        return str(datetime.now()).replace(':','').replace('.','')

    @property
    def getpath(self):
        self.__ruta='Distribuidores'+os.sep+self.__user+os.sep+self.FECHA[0:10]
        return  self.__ruta

    def argumentos(self):
        self.config.read('config.ini')
        for i in self.config.sections():
            self._parser.add_argument('-'+i,action="store_const",const=12,help=f"visualzar GDD para el dz {i}")

    def credenciales(self):
        for key,value in vars(self._parser.parse_args()).items():
            if value is not None:
                self.setterUSER=self.config.get(key.upper(),'USER')
                self.settPASS=self.config.get(key.upper(),'PASS')

    def directorioRuta(self,ruta):
        if 'Distribuidores' not in os.listdir() or self.USER not in os.listdir(path=configuracion._path) or self.FECHA not in os.listdir(path=os.path.join(configuracion._path,self.__user)) or ruta not in os.listdir(path=os.path.join(configuracion._path,self.__user,self.FECHA)) :
              os.makedirs(os.path.join(self.getpath,ruta),mode=7,exist_ok=True)
        self.__ruta+=os.path.sep+ruta
        return self.__ruta

import importlib
from rich.console import Console
from core.Interfaces.Iplugins import IPluging
from typing import Self
from .util import  loadplugin
import os


class MyApplication:

    __VERSION = '0.1'
    __plugin = []
    _Console = Console()
    _currentModule=None
        
    def __new__(cls) -> Self:
        modules={'defaul':importlib.import_module('default.defult')}
        for  i in os.listdir('plugins'):
            modules[i]=loadplugin(i)
        
        cls.__plugin.append(modules)
        return object.__new__(cls)

    @property
    def plugins(self):
        return self.__plugin

    @property
    def getmodulo(self) -> IPluging:
        return self._currentModule.Plugin()

    def search_module(self,name): 
        try:
            for i in self.__plugin:
                self._currentModule=i[name]
                break            
        except:
            raise 'error no se encontro el modulo' 

    def run(self,pregunta) -> None:
        try:
            while True:
                self.search_module(pregunta)
                self.getmodulo.execute(self._Console)
        except ModuleNotFoundError as e:
            print(e)
        except BaseException as e :
            print(e)       

    def update(self):
        import requests
        version = requests.get('')
        if self.__VERSION != version:
            pass


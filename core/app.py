import os
import questionary
from typing import List
from .util import  loadplugin,PLUGIN_PACKAGE
from core.Interfaces.Iplugins import IPluging

class MyApplication:

    __VERSION = '0.1'
    _currentModule=None        

    @classmethod
    def plugins(cls) ->List:      
        return list(map( lambda  i: {i:loadplugin(i)}, os.listdir(PLUGIN_PACKAGE)) )

    @classmethod
    def get_current_module(cls) -> IPluging:
        return cls._currentModule.Plugin()

    @classmethod
    def find_module_by_name(cls,name): 
        "Se busca el modolo selecionado y se retorna su directorio"
        module_found = any(name in i for i in cls.plugins())
        if module_found:
            cls._currentModule = next(i for i in cls.plugins() if name in i)[name]
        else:
            raise ValueError(f'Módulo {name}no encontrado')

    @classmethod
    def run(cls) -> None:
        while True:
            cls.find_module_by_name( questionary.rawselect( message="SELECCIONE EL MODULO A USAR: ",
                                                            choices=sorted(os.listdir(PLUGIN_PACKAGE), 
                                                            reverse=True)
                                                           ).ask())
            cls.get_current_module().execute(questionary)

    def update(self):
        import requests
        version = requests.get('')
        if self.__VERSION != version:
            pass


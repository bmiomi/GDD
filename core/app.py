import importlib
import questionary
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
        

    @classmethod
    def plugins(cls):
        modules={}        
        for  i in os.listdir('plugins'):
            modules[i]=loadplugin(i)
        cls.__plugin.append(modules)
        return cls.__plugin

    @classmethod
    def getmodulo(cls) -> IPluging:
        return cls._currentModule.Plugin()

    @classmethod
    def search_module(cls,name): 
        "Se busca el modolo selecionado y se retorna su directorio"
        module_found = list(filter(lambda i: name in i, cls.plugins()))
        if module_found:
            cls._currentModule = module_found[0][name]
        else:
            raise ValueError('Módulo no encontrado')

    @classmethod
    def run(cls) -> None:
        while True:
            cls.search_module( questionary.rawselect( message="SELECCIONE EL MODULO A USAR: ", choices=sorted(os.listdir("plugins"), reverse=True)).ask())
            cls.getmodulo().execute(questionary,cls._Console)

    def update(self):
        import requests
        version = requests.get('')
        if self.__VERSION != version:
            pass


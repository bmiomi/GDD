from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
import questionary
from core.Interfaces.Iplugins import IPluging
from .src.modules.config import ConfigFactory
from .src import XsalesFactory
from .util import scandir,sep
@dataclass
class Data:

    Turno:str=None
    Opcion:Optional[str]=None
    ContenedorDZ:Optional[List]=None
    dato:Optional[str]=None 

def preguntass(nombremodulo:str,questionari: questionary,config:ConfigFactory) -> List[Dict]:    

   uno=questionari.rawselect('selecciona el turno que te toca',choices=config.Turnos).ask()

   dos=questionari.rawselect('Selecione el proceso a realizar',choices=config.Revisiones).ask()

   tres=questionari.checkbox('Seleccione Server',choices=config.Dz({'Opcion':dos,'Turno':uno})).ask()

   return {'Turno':uno,'Opcion':dos,'ContenedorDZ':tres}


class Plugin(IPluging):

    __submodulo=None
    __config=None
    __question:Dict= {
            'type': 'rawlist',
            'name': 'Modulo',
            'message': "Que Sub Modulo de Xsales desea ? ",
            'choices': [i.name for i in scandir ( f'.{sep}plugins{sep}xsales{sep}src{sep}modules') if i.is_dir() and i.name!='__pycache__']
        }

    @property
    def nombre(self) -> str:
        return 'Xsales'

    @property
    def question(self):
        return self.__question

    @property
    def getsubmodule(self):
        return (self.__config,self.__submodulo)

    @getsubmodule.setter
    def getsubmodule(self,value):
        self.__submodulo =XsalesFactory.getModulo(value)
        self.__config=ConfigFactory.getModulo(value)
        self.__config.Revisiones=value

    def execute(self,question,console):

        config,modulo,=self.getsubmodule

        resp=preguntass(self.getsubmodule,question,config)

        data=Data(**resp)

        with console.status(f'Procesando....',spinner=self.getsubmodule[0].spinner
                                    ):            
            s=self.getsubmodule[1](data,self.getsubmodule[0])
            s.mostrar_info( console)


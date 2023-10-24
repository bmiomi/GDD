from typing import Callable, Dict, List, Optional
from dataclasses import dataclass

import questionary

from core.Interfaces.Iplugins import IPluging
from .src.modules.config import ConfigFactory
from .src import XsalesFactory
from .src.util import scandir,sep

@dataclass
class Data:

    Turno:str=None
    Opcion:Optional[str]=None
    ContenedorDZ:Optional[List]=None
    dato:Optional[str]=None 
    questionary:Callable=None
    console:Callable=None


class Plugin(IPluging):

    __modulos:List[Dict] = {
            'type': 'rawlist',
            'name': 'Modulo',
            'message': "Que Sub Modulo de Xsales desea ? ",
            'choices': [i.name for i in scandir (f'.{sep}plugins{sep}xsales{sep}src{sep}modules') if i.is_dir() and i.name!='__pycache__']
        }
    
    @property
    def nombre(self) -> str:
        return 'Xsales'

    def execute(self,question,consola):
        SModulo=question.prompt(self.__modulos)
        main(SModulo,question,consola)





def preguntass(nombremodulo:str,questionari: questionary,config:ConfigFactory) -> List[Dict]:    

   uno=questionari.rawselect('selecciona el turno que te toca',choices=config.Turnos).ask()

   dos=questionari.rawselect('Selecione el proceso a realizar',choices=config.Revisiones).ask()

   tres=questionari.checkbox('Seleccione Server',choices=config.Dz({'Opcion':dos,'Turno':uno})).ask()

   return {'Turno':uno,'Opcion':dos,'ContenedorDZ':tres}


def main(nombremodulo: dict,*args) ->None:
    
    questionari,console = args

    modulo =XsalesFactory.getModulo(nombremodulo)

    config=ConfigFactory.getModulo(nombremodulo)
    config.Revisiones=nombremodulo

    resp=preguntass(nombremodulo,questionari,config)

    resp['console']=console
    
    data=Data(**resp)

    with console.status('Procesando..',spinner=config.spinner):
        xsales=modulo(data,config)
        xsales.mostrar_info()


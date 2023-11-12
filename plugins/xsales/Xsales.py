from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
import questionary

from core.Interfaces.Iplugins import IPluging
from .config import Config
from .src import XsalesFactory
from .util import scandir,sep

@dataclass
class Data:

    Turno:str=None
    Opcion:Optional[str]=None
    ContenedorDZ:Optional[List]=None
    dato:Optional[str]=None 
    questionary:Callable=None
    consola:Callable=None


def preguntass(config:Config) ->Dict:    

   uno=questionary.rawselect('selecciona el turno que te toca',choices=config.Turnos).ask()
   dos=questionary.rawselect('Selecione el proceso a realizar',choices=config.Revisiones).ask()
   tres=questionary.checkbox('Seleccione Server',choices=config.Dz({'Opcion':dos,'Turno':uno})).ask()
   return {'Turno':uno,'Opcion':dos,'ContenedorDZ':tres}

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

        #objeto a retornar
        modulo =XsalesFactory.getModulo(value=SModulo) 

        #asignamos el nombre del modulo a la configuracion
        modulo.config.Revisiones=SModulo 

        #realizamos las preguntas
        resp=preguntass(modulo.config)
        data=Data(**resp)
        modulo.dato=data
        with consola.status('Procesando..',spinner=modulo.config.spinner):
            for namedz in data.ContenedorDZ:
                consola.log(modulo.mostrar_info(namedz))
                
from typing import  Dict, List, Optional
from dataclasses import dataclass
import questionary
from .confi import Config

@dataclass
class Data:

    Turno:str=None
    Opcion:Optional[str]=None
    ContenedorDZ:Optional[List]=None
    dato:Optional[str]=None 

def preguntass(config:Config) ->Dict:    

   uno=questionary.rawselect('selecciona el turno que te toca',choices=config.Turnos,).ask()
   questionary.Separator('esto es un separetor')
   dos=questionary.rawselect('Selecione el proceso a realizar',choices=config.Revisiones).ask()
   tres=questionary.checkbox('Seleccione Server',choices=config.Dz({'Opcion':dos,'Turno':uno})).ask()

   return {'Turno':uno,'Opcion':dos,'ContenedorDZ':tres}

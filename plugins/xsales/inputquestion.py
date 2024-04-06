from typing import  Dict, List, Optional
from dataclasses import dataclass
from .confi import Config

@dataclass
class Data:

    Turno:str=None
    Opcion:str=None
    ContenedorDZ:List=None
    # dato:Optional[str]=None 

def preguntass(questionary,config:Config) ->Dict:  
   uno=questionary.rawselect('selecciona el turno que te toca',choices=config.Turnos,).ask()
   dos=questionary.rawselect('Selecione el proceso a realizar',choices=config.Revisiones).ask()
   tres=questionary.checkbox('Seleccione Server',choices=config.Dz({'Opcion':dos,'Turno':uno})).ask()
   return Data(**{'Turno':uno,'Opcion':dos,'ContenedorDZ':tres})

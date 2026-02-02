from typing import  Dict, List, Optional
from dataclasses import dataclass

import questionary
from .src.config import Config

@dataclass
class Data:

    Turno:str=None
    Opcion:str=None
    ContenedorDZ:List=None
    dato:Optional[str]=None 
    reporte:str=None

def preguntass(questionary:questionary,config:Config) ->Data:  
   uno=questionary.rawselect('selecciona el turno que te toca',choices=config.Turnos,).ask()
   dos=questionary.rawselect('Selecione el proceso a realizar',choices=config.Revisiones).ask()
   tres=questionary.checkbox('Seleccione Server',choices=config.Dz({'Opcion':dos,'Turno':uno})).ask()
   cuatro=questionary.confirm('Desea Gerarar un excel de la informacion generada',).ask()
   return Data(**{'Turno':uno,'Opcion':dos,'ContenedorDZ':tres,'reporte':cuatro})

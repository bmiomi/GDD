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
    parametros_usuario: Dict[str, str] = None

def preguntass(questionary:questionary,config:Config) ->Data:  
   uno=questionary.rawselect('selecciona el turno que te toca',choices=config.Turnos,).ask()
   
   # Obtener nombres de consultas del config (no de Revisiones)
   consultas = config.configConsultasStructured
   nombres_consultas = list(consultas.keys())
   
   dos=questionary.rawselect('Selecione el proceso a realizar',choices=nombres_consultas).ask()
   tres=questionary.checkbox('Seleccione Server',choices=config.Dz({'Opcion':dos,'Turno':uno}), validate=lambda x: len(x) > 0 or "Debe seleccionar al menos un servidor").ask()
   
   # Preguntar por parámetros de usuario si la consulta los requiere
   parametros_usuario = {}
   if dos in consultas:
       params_usuario = consultas[dos].get('parametros_usuario', [])
       for param in params_usuario:
           # Parámetros obligatorios - validar que no sean vacíos
           respuesta = questionary.text(
               f'Ingrese valor para {param}:',
               validate=lambda x: len(x) > 0 or f"El parámetro '{param}' es obligatorio"
           ).ask()
           parametros_usuario[param] = respuesta
   
   cuatro=questionary.confirm('Desea Gerarar un excel de la informacion generada',).ask()
   return Data(**{'Turno':uno,'Opcion':dos,'ContenedorDZ':tres,'reporte':cuatro, 'parametros_usuario': parametros_usuario})

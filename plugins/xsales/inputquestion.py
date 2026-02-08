from typing import Dict, List, Optional, Literal
from dataclasses import dataclass

import questionary
from .src.config import Config
from .src.questions import CommonQuestions
from core.models import PreferenceData

@dataclass
class Data:

    Turno:str=None
    Opcion:str=None
    ContenedorDZ:List=None
    dato:Optional[str]=None 
    reporte:str=None
    parametros_usuario: Dict[str, str] = None
    action: str = 'query'  # 'query' o 'configure'

def preguntass(questionary: questionary, config: Config, preferences: PreferenceData = None) -> Data:
   # Obtener nombres de consultas del config (no de Revisiones)
   consultas = config.configConsultasStructured
   nombres_consultas = list(consultas.keys())

   def _is_back_input(value: Optional[str]) -> bool:
       if value is None:
           return False
       return value.strip().lower() in {"volver", "back", "<< volver"}

   while True:
       turno = CommonQuestions.ask_turno(questionary, config.Turnos)
       if turno is None:
           return Data(action='back')

       while True:
           opcion = CommonQuestions.ask_proceso(questionary, nombres_consultas)
           if opcion is None:
               break

           while True:
               contenedor_dz = CommonQuestions.ask_distribuidores(
                   questionary,
                   config.Dz({'Opcion': opcion, 'Turno': turno}),
                   mensaje='Seleccione Server',
                   validate=lambda x: (
                       (CommonQuestions.BACK_OPTION in x) or len(x) > 0
                   ) or "Debe seleccionar al menos un servidor"
               )
               if contenedor_dz is None:
                   break

               # Preguntar por parámetros de usuario si la consulta los requiere
               parametros_usuario: Dict[str, str] = {}
               if opcion in consultas:
                   params_usuario = consultas[opcion].get('parametros_usuario', [])
                   back_to_dz = False
                   for param in params_usuario:
                       respuesta = questionary.text(
                           f'Ingrese valor para {param} (o escriba "volver" para regresar):',
                           validate=lambda x: len(x) > 0 or f"El parámetro '{param}' es obligatorio"
                       ).ask()
                       if _is_back_input(respuesta):
                           back_to_dz = True
                           break
                       parametros_usuario[param] = respuesta
                   if back_to_dz:
                       continue

               # Si hay preferencias guardadas, usar eso en lugar de preguntar
               if preferences:
                   reporte = preferences.generate_excel
               else:
                   reporte = CommonQuestions.ask_generar_reporte(
                       questionary,
                       mensaje='Desea Gerarar un excel de la informacion generada'
                   )

               return Data(
                   **{
                       'Turno': turno,
                       'Opcion': opcion,
                       'ContenedorDZ': contenedor_dz,
                       'reporte': reporte,
                       'parametros_usuario': parametros_usuario,
                       'action': 'query'
                   }
               )


def menu_principal(questionary: questionary, config: Config, preferences: PreferenceData = None) -> Data:
    """Menú principal que permite elegir entre ejecutar o configurar."""
    while True:
        accion = questionary.select(
            'Server XSales',
            choices=['Ejecutar consulta', 'Configurar', 'Salir']
        ).ask()

        if accion == 'Configurar':
            return Data(action='configure')
        if accion == 'Salir':
            return Data(action='exit')

        data = preguntass(questionary, config, preferences)
        if data.action == 'back':
            continue
        return data

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
from .config import ConfigFactory
from .src import XsalesFactory
from .util import scandir


class Plugin:

    question:List[Dict] = {
            'type': 'rawlist',
            'name': 'Modulo',
            'message': "Que Sub Modulo de Xsales desea ? ",
            'choices': [i.name for i in scandir ('.\\plugins\\xsales\\src\\modules') if i.is_dir() and i.name!='__pycache__']
        }
    
    @property
    def nombre(self) -> str:
        return 'Xsales'

    def execute(self,question,consola):
        SModulo=question.prompt(self.question)
        main(SModulo,question,consola)

@dataclass
class Data:

    ContenedorDZ:Optional[List]=None
    Turno:str=None
    Opcion:Optional[str]=None
    dato:Optional[str]=None 
    questionary:Callable=None
    console:Callable=None

def preguntas(nombremodulo:str,questionari:Callable,config:ConfigFactory) -> List[Dict]:

    questions=[]

    if nombremodulo == 'Server':

        questions= [
            {
                'type': 'rawlist',
                'name': 'Opcion',
                'message': 'SELECCIONE PROCESO A REALIZAR',
                'choices': ['REVICION_MADRUGADA', 
                            'DESC.DIURNOS', 
                            'DESC.NOCTURNOS',
                            'VALIDAR_ClIENTE', 
                            'Total_Pedidos'
                           ]
            },
          
            {
                'type': 'rawlist',
                'name': 'Turno',
                'message': 'selecciona el turno que te toca',
                'choices': ['TECNICO 3-AM','TECNICO(1) 4-AM','TECNICO(2) 4-AM'],
                'when': lambda answers: answers['Opcion']== 'REVICION_MADRUGADA'
            },

            {
                'type': 'checkbox',
                'name': 'ContenedorDZ',
                'message': 'Seleccione Server',
                'choices': lambda answers: config.Dz(answers),
                'when': lambda answers: answers['Opcion'] == 'REVICION_MADRUGADA',
                'validate':lambda a: (True if len(a) > 0 else "Debes seleccionar almenos un Dz/regional")
            },


            {
                'type': 'checkbox',
                'name': 'ContenedorDZ',
                'message': 'Selecionar DZ/DIRECTA que deseas revisar',
                'when': lambda answers: answers['Opcion'] != 'REVICION_MADRUGADA',
                'choices': config.Dz(),
                'validate':lambda a: (True if len(a) > 0 else "Debes seleccionar almenos un Dz/regional")
            },
        {
                'type': 'input',
                'name': 'dato',
                'message': 'Ingrese la CI/RUC del cliente',
                'when': lambda answers: answers['Opcion'] == 'VALIDAR_ClIENTE',
                'validate':lambda a: (True if len(a) > 0 else "Debes Ingresar un valor")

            },

        ]

    if nombremodulo == 'FTP':

        questions= [

            {
                'type': 'rawlist',
                'name': 'Opcion',
                'message': 'SELECCIONE PROCESO A REALIZAR',
                'choices': ['Validar DESC', 'Validar Maestros', 'Descargar Base']
            },

            {
                'type': 'rawlist',
                'name': 'Turno',
                'message': 'selecciona el turno que te toca',
                'choices': ['TECNICO 3-AM','TECNICO(1) 4-AM','TECNICO(2) 4-AM'],
                'when': lambda answers: answers['Opcion']== 'Validar DESC'
            },

            {
                'type': 'checkbox',
                'name': 'ContenedorDZ',
                'message': 'Seleccione Server',
                'choices': lambda answers: config.Dz(answers),
                'when': lambda answers: answers['Opcion'] == 'Validar DESC',
                'validate':lambda a: (True if len(a) > 0 else "Debes seleccionar almenos un Dz/regional")
            },

            {
                'type': 'checkbox',
                'name': 'ContenedorDZ',
                'message': 'Selecione el dz que desea revisar?',
                'choices': config.Dz(),
                'when': lambda answers: answers['Opcion'] == 'Descargar Base',
                'validate':lambda a: (True if len(a) == 1 else "Debes seleccionar un Dz/regional"),
            },
            {
                'type': 'checkbox',
                'name': 'ContenedorDZ',
                'message': 'selecione servers',
                'when':lambda answes: answes['Opcion']=='Validar Maestros',
                'choices': ['Xsales','Pronaca'],
                'validate':lambda a: (True if len(a) > 0 else "Debes seleccionar almenos un Dz/regional")

            }

        ]

    if nombremodulo == 'Status':
        questions=[
            {
                'type': 'input',
                'name': 'Opcion',
                'message': 'SELECCIONE PROCESO A REALIZAR',
            }]

    return questionari.prompt(questions)

def main(respusta: dict,*args) ->None:

    questionari,console = args
    nombremodulo = respusta.get('Modulo')
    modulo = XsalesFactory.getModulo(nombremodulo)
    config=ConfigFactory.getModulo(nombremodulo)
    resp=preguntas(nombremodulo,questionari,config)
    resp['console']=console
    data=Data(**resp)
    with console.status('Procesando..',spinner=config.spinner):
        xsales=modulo(data,config)
        xsales.mostrar_info()


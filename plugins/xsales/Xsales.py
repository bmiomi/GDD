<<<<<<< HEAD
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
=======
from typing import Callable, Dict, List, Optional
from dataclasses import dataclass

>>>>>>> 032df41845b8e8a9de39f97ab6d64a0114e459b2
import questionary
from core.Interfaces.Iplugins import IPluging
from .config import Config
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


<<<<<<< HEAD
def preguntass(config:Config) ->Dict:    
=======
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
>>>>>>> 032df41845b8e8a9de39f97ab6d64a0114e459b2

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

<<<<<<< HEAD

class Plugin(IPluging):

    __submodulo=None
    __config=None
    __question:Dict= {
            'type': 'rawlist',
            'name': 'Modulo',
            'message': "Que Sub Modulo de Xsales desea ? ",
            'choices': [i.name for i in scandir ('.\\plugins\\xsales\\src\\modules') if i.is_dir() and i.name!='__pycache__']
        }

    @property
    def nombre(self) -> str:
        return 'Xsales'

    def execute(self,question,consola):
        SModulo=question.prompt(self.__submodulo)
        main(SModulo,question,consola)
=======
>>>>>>> 032df41845b8e8a9de39f97ab6d64a0114e459b2

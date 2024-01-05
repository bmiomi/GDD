from typing import Dict, List

from core.Interfaces.Iplugins import IPluging
from plugins.xsales.inputquestion import Data, preguntass
from .src import XsalesFactory
from .util import scandir,sep

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

        # with consola.status('Procesando..',spinner=modulo.config.spinner):
            # for namedz in data.ContenedorDZ:
        # print(data.ContenedorDZ)
        modulo.mostrar_info(data.ContenedorDZ,consola)

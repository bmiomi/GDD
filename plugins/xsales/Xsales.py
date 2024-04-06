from ast import mod
from cgitb import small
import os
from typing import Dict, List

from core.Interfaces.Iplugins import IPluging
from .inputquestion import Data, preguntass
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
  
        try:
            print('*'*10)
            SModulo=question.prompt(self.__modulos)
            #objeto a retornar
            modulo =XsalesFactory.getModulo(value=SModulo.get('Modulo')) 
            #realizamos las preguntas
            resp=preguntass(question,modulo.config)

            modulo.dato=resp
            print(resp)

            for namedz in resp.ContenedorDZ:
                modulo.mostrar_info(namedz,consola)

        except BaseException as e :
            print ('s:'+e)
            pass
        except KeyboardInterrupt:
            return 0       
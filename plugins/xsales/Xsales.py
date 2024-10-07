from typing import Dict, List
from core.Interfaces.Iplugins import IPluging
from .inputquestion import  preguntass
from .src import XsalesFactory
from .util import scandir,path

class Plugin(IPluging):


    __modulo_dir = path.join(path.dirname(path.abspath(__file__)),'src', 'modules')

    __modulos:List[Dict] = [
        
        {
            'type': 'rawlist',
            'name': 'Modulo',
            'message': "SELECIONE UNA OPCION",
            'choices': [i.name for i in scandir(__modulo_dir) if i.is_dir()]

        }
        ]
    
    @property
    def nombre(self) -> str:
        return 'Xsales'
    
    def execute(self,question):  
        try:
            SModulo=question.prompt(self.__modulos)
            #objeto a retornar
            modulo =XsalesFactory.getModulo(value=SModulo.get('Modulo')) 
            #realizamos las preguntas
            resp=preguntass(question,modulo.config)

            modulo.dato=resp

            modulo.mostrar_info(resp.ContenedorDZ,self.console)
            modulo.msd(self.console)
            modulo.generararchivo(resp.reporte,resp.Opcion,self.console)

        except BaseException as e :
            print (f'{e}')
        except KeyboardInterrupt:
            return 0       
        

    
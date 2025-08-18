from typing import Dict, List
from core.Interfaces.Iplugins import IPluging
from .inputquestion import  preguntass
from .src import XsalesFactory
from .util import scandir,sep,path

class Plugin(IPluging):

    __modulo_dir = path.join(path.dirname(path.abspath(__file__)),'src', 'modules')

    __modulos:List[Dict] = {
            'type': 'rawlist',
            'name': 'Modulo',
            'message': "Que Sub Modulo de Xsales desea ? ",
            'choices': [i.name for i in scandir(__modulo_dir) if i.is_dir()]
        }
        
    @property
    def nombre(self) -> str:
        return 'Xsales'
    

    def execute(self,question):  
        try:
            SModulo=question.prompt(self.__modulos)
            #objeto a retornar
            modulo =XsalesFactory.getModulo(value=SModulo.get('Modulo')) 
            #realizamos las preguntas
            modulo.dato=preguntass(question,modulo.config)

            modulo.mostrar_info(modulo.dato.ContenedorDZ,self.console)

            modulo.generararchivo(modulo.dato.reporte,modulo.dato.Opcion,self.console)

        except BaseException as e :
            print (f's:{e.__class__.__name__}{e}')
        except KeyboardInterrupt:
            return 0       

    #esta subido el archivo
    

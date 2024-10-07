<<<<<<< HEAD
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
        

    
=======
from typing import Dict, List
from core.Interfaces.Iplugins import IPluging
from .inputquestion import  preguntass
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
            SModulo=question.prompt(self.__modulos)
            #objeto a retornar
            modulo =XsalesFactory.getModulo(value=SModulo.get('Modulo')) 
            #realizamos las preguntas
            modulo.dato=preguntass(question,modulo.config)

            modulo.mostrar_info(modulo.dato.ContenedorDZ,consola)

            modulo.generararchivo(modulo.dato.reporte,modulo.dato.Opcion,consola)

        except BaseException as e :
            print (f's:{e.__class__.__name__}{e}')
        except KeyboardInterrupt:
            return 0       

    #esta subido el archivo
    
>>>>>>> 8be410330e0e34aa49b9dec88801aabcfc683771

import importlib
import os
from types import ModuleType
import questionary
from rich.console import Console

from core.Interfaces.Iplugins import IPluging
from default.defult import Default

def loadplugin(plugin: str) -> ModuleType:
    plugin_module_path = f'plugins.{plugin.lower()}.{plugin.title()}'
    modulo = importlib.import_module(plugin_module_path)
    return modulo

class MyApplication:

    __VERSION = '0.1'
    __plugin = None
    _question = questionary
    _Console = Console()

    @property
    def question(self):
        return self._question

    def search_module(self, nmodele):
        self.name = nmodele
        if nmodele:
            self.__plugin = loadplugin(nmodele)
        else:
            self.__plugin = [importlib.import_module('default.defult')][0]

    def getmodulo(self) -> IPluging:
        # if isinstance(self.__plugin.Default(),Default):
        #     return self.__plugin.Default()
        return self.__plugin.Plugin()

    def questions(self, question) -> None:
        modulo = question
        if modulo == 0:
            exit()
        self.search_module(modulo)

    def run(self) -> None:

        pregunta:str=questionary.rawselect('SELECCIONE EL MODULO A USAR:',choices=sorted(os.listdir('plugins'), reverse=True)).ask()
        self.questions(pregunta)
        # obtenemos una instancia del modulo a usar
        plugin = self.getmodulo()    
        # realizamos las preguntantas asociadas a ese modulo.
        Smodulo=questionary.prompt(plugin.question)
        #seteamos el submodulo0
        plugin.getsubmodule=Smodulo                     
        respuesta=plugin.execute(self.question)
        # while True:
        with self._Console.status(f'Procesando....',
                                    spinner=plugin.getsubmodule[0].spinner
                                    ):
            
            s=plugin.getsubmodule[1](respuesta,plugin.getsubmodule[0])
            s.mostrar_info()
            self._Console.log(*s.message,style=s.status,sep='\n')




if __name__ == "__main__":

    try:
        app = MyApplication()
        app.run()

    except ModuleNotFoundError as e:
        print(f'hay un error faltan dependecias por instalar {e}')
    # except BaseException as e :
    #     print(f'Se encontro un error GRAVE QUE IMPIDE LA EJECUCION DEL PROGRAMA REPORTAR AL ADMINISTRADOR: {e}')

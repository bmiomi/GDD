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
    __plugin = [importlib.import_module('default.defult')]
    _Console = Console()

    @property
    def question(self):
        return questionary

    def search_module(self,name):
        self.name=name
        if self.name:
            self.__plugin = loadplugin(self.name)

    def getmodulo(self) -> IPluging:
        return self.__plugin.Plugin()
# lorena segura
    @staticmethod
    def run(self) -> None:

        while True:
            
            myapp=self.__plugin[0]
            # myapp.Default().execute(questionary)
            # if not myapp.Default().estado:
            #     break
            self.search_module('Xsales')
            plugin = self.getmodulo()
            plugin.execute(self.question, self._Console)


    def update(self):
        import requests
        version = requests.get('')
        if self.__VERSION != version:
            pass


if __name__ == "__main__":

    try:
        MyApplication.run(MyApplication())
    except ModuleNotFoundError as e:
        raise f'hay un error faltan dependecias por instalar {e}'
    except BaseException as e :
        print(f'Se encontro un error GRAVE QUE IMPIDE LA EJECUCION DEL PROGRAMA REPORTAR AL ADMINISTRADOR: {e}')

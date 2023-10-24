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
    __question = questionary
    _Console = Console()

    @property
    def question(self):
        return self.__question

    def search_module(self):
        if self.name:
            self.__plugin = loadplugin(self.name)
        else:
            self.__plugin = [importlib.import_module('mai')][0]


    def getmodulo(self) -> IPluging:
        return self.__plugin.Plugin()


    def run(self) -> None:

        Default().execute(questionary)

        # while True:

        #     self.name = self.question.rawselect('SELECCIONE EL MODULO A USAR:',choices=sorted(os.listdir('plugins'), reverse=True)).ask()
        #     self.search_module()
        #     plugin = self.getmodulo()

        #     plugin.execute(self.question, self._Console)

    def update(self):
        import requests
        version = requests.get('')
        if self.__VERSION != version:
            pass


if __name__ == "__main__":

    try:
        MyApplication().run()
    except ModuleNotFoundError as e:
        print(f'hay un error faltan dependecias por instalar {e}')
    except BaseException as e :
        print(f'Se encontro un error GRAVE QUE IMPIDE LA EJECUCION DEL PROGRAMA REPORTAR AL ADMINISTRADOR: {e}')

import importlib
import os

from types import ModuleType
import questionary
from rich.console import Console
"alan me cae mal"

from core.Interfaces.Iplugins import IPluging

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
            self.__plugin = [importlib.import_module('mai')][0]


    def getmodulo(self) -> IPluging:
        return self.__plugin.Plugin()

    def questions(self, question) -> None:
        modulo = question.get('Modulo', 0)
        if modulo == 0:
            exit()
        self.search_module(modulo)

    def run(self) -> None:

        while True:

            pregunta = self.question.prompt(
                [
                    {
                        'name': 'Modulo',
                        'type': 'rawlist',
                        'message': 'SELECCIONE EL MODULO A USAR: ',
                        'choices': sorted(os.listdir('plugins'), reverse=True)
                    }
                ]
            )

            self.questions(pregunta)
            plugin = self.getmodulo()
            plugin.execute(self.question, self._Console)


    def update(self):
        import requests
        version = requests.get('')
        if self.__VERSION != version:
            pass


if __name__ == "__main__":

    try:
        app = MyApplication()
        app.run()


    except ModuleNotFoundError as e:
        print(f'hay un error faltan dependecias por instalar {e}')

    # except BaseException as e :
    #     print(f'Se encontro un error GRAVE QUE IMPIDE LA EJECUCION DEL PROGRAMA REPORTAR AL ADMINISTRADOR: {e}')

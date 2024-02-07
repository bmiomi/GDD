import importlib
from types import ModuleType


def loadplugin(plugin: str) -> ModuleType:
    plugin_module_path =  f'plugins.{plugin.lower()}.{plugin.title()}'
    modulo = importlib.import_module(plugin_module_path)
    return modulo

import importlib
from types import ModuleType


def loadplugin(plugin: str) -> ModuleType:
    return importlib.import_module(f'plugins.{plugin.lower()}.{plugin.title()}')

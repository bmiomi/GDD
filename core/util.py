import importlib
from types import ModuleType

from core.exepcions.exception import PluginLoadError

PLUGIN_PACKAGE='plugins'

def loadplugin(plugin_name: str) -> ModuleType:
    try:
        return importlib.import_module(f'{PLUGIN_PACKAGE}.{plugin_name.lower()}.{plugin_name.title()}')
    except ImportError as e:
        raise PluginLoadError(f'Error al cargar el plugin {plugin_name}: {e}')

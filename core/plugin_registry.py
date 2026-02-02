"""
Registro centralizado de plugins.
Gestiona descubrimiento, validación y acceso a plugins.
"""
from typing import Dict, Type, List, Optional
from pathlib import Path
import importlib.util
from .Interfaces.plugin import IPlugin, PluginMetadata, PluginStatus
from rich.console import Console


class PluginRegistry:
    """
    Registro centralizado de plugins.
    
    Responsabilidades:
    - Autodescubrimiento de plugins en carpeta 'plugins/'
    - Registro manual de plugins
    - Validación de plugins
    - Gestión de instancias (singleton por plugin)
    - Acceso a metadata
    
    Uso:
        registry = PluginRegistry()
        registry.discover()
        
        plugins = registry.list_plugins()
        plugin = registry.get('xsales')
        plugin.execute()
    """
    
    def __init__(self, console: Optional[Console] = None):
        """
        Inicializa el registro de plugins.
        
        Args:
            console: Consola para logging (opcional)
        """
        self._plugins: Dict[str, Type[IPlugin]] = {}
        self._instances: Dict[str, IPlugin] = {}
        self._metadata: Dict[str, PluginMetadata] = {}
        self._console = console or Console()
    
    def discover(self, plugin_dir: str = "plugins") -> List[str]:
        """
        Descubre plugins automáticamente.
        
        Escanea la carpeta 'plugins/' buscando archivos plugin.py
        que contengan clases que hereden de IPlugin.
        
        Convención:
        - plugins/miplugin/plugin.py
        - class MiPlugin(IPlugin)
        
        Args:
            plugin_dir: Directorio donde buscar plugins
        
        Returns:
            Lista de nombres de plugins descubiertos
        """
        discovered = []
        plugin_path = Path(plugin_dir)
        
        if not plugin_path.exists():
            self._console.log(f"[yellow]⚠ Directorio de plugins no encontrado: {plugin_dir}")
            return discovered
        
        for plugin_folder in plugin_path.iterdir():
            if not plugin_folder.is_dir():
                continue
            
            if plugin_folder.name.startswith('_') or plugin_folder.name.startswith('.'):
                continue
            
            # Buscar plugin.py
            plugin_file = plugin_folder / "plugin.py"
            
            # Fallback: buscar archivo con nombre capitalizado (legacy)
            if not plugin_file.exists():
                plugin_file = plugin_folder / f"{plugin_folder.name.title()}.py"
            
            if not plugin_file.exists():
                continue
            
            # Cargar plugin
            try:
                plugin_name = self._load_plugin(plugin_folder.name, plugin_file)
                if plugin_name:
                    discovered.append(plugin_name)
            except Exception as e:
                self._console.log(f"[red]✗ Error cargando plugin {plugin_folder.name}: {e}")
        
        return discovered
    
    def _load_plugin(self, folder_name: str, file_path: Path) -> Optional[str]:
        """
        Carga un plugin desde archivo.
        
        Args:
            folder_name: Nombre de la carpeta del plugin
            file_path: Ruta al archivo del plugin
        
        Returns:
            Nombre del plugin si se cargó exitosamente, None si no
        """
        spec = importlib.util.spec_from_file_location(
            f"plugins.{folder_name}",
            file_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Buscar clase que implemente IPlugin
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, IPlugin) and 
                attr is not IPlugin):
                
                # Registrar plugin
                instance = attr()
                metadata = instance.metadata
                
                self._plugins[metadata.name] = attr
                self._metadata[metadata.name] = metadata
                
                self._console.log(f"[green]✓ Plugin cargado: {metadata}")
                
                return metadata.name
        
        return None
    
    def register(self, plugin_class: Type[IPlugin]) -> None:
        """
        Registro manual de plugin.
        
        Args:
            plugin_class: Clase del plugin a registrar
        """
        instance = plugin_class()
        metadata = instance.metadata
        
        self._plugins[metadata.name] = plugin_class
        self._metadata[metadata.name] = metadata
        
        self._console.log(f"[blue]→ Plugin registrado: {metadata}")
    
    def get(self, name: str) -> IPlugin:
        """
        Obtiene instancia de plugin (singleton).
        
        Args:
            name: Nombre del plugin
        
        Returns:
            Instancia del plugin
        
        Raises:
            ValueError: Si el plugin no existe
        """
        if name not in self._instances:
            if name not in self._plugins:
                available = ', '.join(self._plugins.keys())
                raise ValueError(
                    f"Plugin '{name}' no encontrado. "
                    f"Disponibles: {available}"
                )
            self._instances[name] = self._plugins[name]()
            self._instances[name].status = PluginStatus.LOADED
        
        return self._instances[name]
    
    def list_plugins(self, enabled_only: bool = True) -> List[PluginMetadata]:
        """
        Lista todos los plugins disponibles.
        
        Args:
            enabled_only: Si True, solo retorna plugins habilitados
        
        Returns:
            Lista de metadata de plugins
        """
        plugins = list(self._metadata.values())
        
        if enabled_only:
            plugins = [p for p in plugins if p.enabled]
        
        return sorted(plugins, key=lambda p: p.name)
    
    def get_metadata(self, name: str) -> Optional[PluginMetadata]:
        """
        Obtiene metadata de un plugin.
        
        Args:
            name: Nombre del plugin
        
        Returns:
            Metadata del plugin o None si no existe
        """
        return self._metadata.get(name)
    
    def exists(self, name: str) -> bool:
        """
        Verifica si existe un plugin.
        
        Args:
            name: Nombre del plugin
        
        Returns:
            True si existe, False si no
        """
        return name in self._plugins
    
    def reload(self, plugin_dir: str = "plugins") -> List[str]:
        """
        Recarga todos los plugins.
        
        Limpia el registro y vuelve a descubrir plugins.
        Útil para desarrollo.
        
        Args:
            plugin_dir: Directorio de plugins
        
        Returns:
            Lista de plugins descubiertos
        """
        self._plugins.clear()
        self._instances.clear()
        self._metadata.clear()
        
        return self.discover(plugin_dir)

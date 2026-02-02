"""
Registro de submódulos de XSales.
Permite autodescubrimiento y registro de submódulos.
"""
from pathlib import Path
from typing import Dict, Type, List, Optional
import importlib.util
from .base_module import XSalesModule, ModuleMetadata


class ModuleRegistry:
    """
    Registro de submódulos de XSales.
    
    Gestiona:
    - Autodescubrimiento de submódulos
    - Registro manual con decorador
    - Acceso a instancias de submódulos
    - Listado de módulos disponibles
    
    Uso:
        # Autodescubrimiento
        module_registry.autodiscover()
        
        # Registro manual
        @ModuleRegistry.register
        class MiModulo(XSalesModule):
            ...
        
        # Obtener módulo
        module = module_registry.get('mimodulo')
    """
    
    _instance: Optional['ModuleRegistry'] = None
    _modules: Dict[str, Type[XSalesModule]] = {}
    _metadata: Dict[str, ModuleMetadata] = {}
    _initialized: bool = False
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, module_class: Type[XSalesModule]):
        """
        Decorador para registro manual de submódulos.
        
        Uso:
            @ModuleRegistry.register
            class MiModulo(XSalesModule):
                ...
        
        Args:
            module_class: Clase del módulo a registrar
        
        Returns:
            La misma clase (para uso como decorador)
        """
        instance = module_class()
        metadata = instance.metadata
        
        cls._modules[metadata.name] = module_class
        cls._metadata[metadata.name] = metadata
        
        return module_class
    
    @classmethod
    def autodiscover(cls, modules_dir: Optional[Path] = None) -> List[str]:
        """
        Autodescubrimiento de submódulos.
        
        Escanea carpetas buscando clases que hereden de XSalesModule.
        
        Convención:
        - modules/FTP/ftp_module.py → class FtpModule(XSalesModule)
        - modules/Server/__init__.py → class ServerModule(XSalesModule)
        
        Args:
            modules_dir: Directorio de módulos (por defecto: directorio actual)
        
        Returns:
            Lista de nombres de módulos descubiertos
        """
        if modules_dir is None:
            modules_dir = Path(__file__).parent
        
        discovered = []
        
        # Escanear subcarpetas
        for module_folder in modules_dir.iterdir():
            if not module_folder.is_dir():
                continue
            
            if module_folder.name.startswith('_') or module_folder.name.startswith('.'):
                continue
            
            # Buscar archivo del módulo
            # Prioridad: {nombre}_module.py > __init__.py
            module_file = module_folder / f"{module_folder.name.lower()}_module.py"
            
            if not module_file.exists():
                module_file = module_folder / "__init__.py"
            
            if not module_file.exists():
                continue
            
            # Cargar módulo
            try:
                module_name = cls._load_module(module_folder.name, module_file)
                if module_name:
                    discovered.append(module_name)
            except Exception as e:
                print(f"Error cargando módulo {module_folder.name}: {e}")
        
        cls._initialized = True
        return discovered
    
    @classmethod
    def _load_module(cls, folder_name: str, file_path: Path) -> Optional[str]:
        """
        Carga un módulo desde archivo.
        
        Args:
            folder_name: Nombre de la carpeta
            file_path: Ruta al archivo del módulo
        
        Returns:
            Nombre del módulo si se cargó exitosamente
        """
        import sys
        
        # Asegurar que el paquete padre esté en sys.modules
        parent_package = 'plugins.xsales.src.modules'
        if parent_package not in sys.modules:
            import plugins.xsales.src.modules
            sys.modules[parent_package] = plugins.xsales.src.modules
        
        module_folder = file_path.parent
        package_name = f"{parent_package}.{folder_name}"

        # Asegurar que el paquete exista para permitir imports internos (ej: plugins...Server.config)
        if package_name not in sys.modules:
            package_init = module_folder / "__init__.py"
            if package_init.exists():
                package_spec = importlib.util.spec_from_file_location(
                    package_name,
                    package_init,
                    submodule_search_locations=[str(module_folder)]
                )
                package_module = importlib.util.module_from_spec(package_spec)
                sys.modules[package_name] = package_module
                try:
                    package_spec.loader.exec_module(package_module)
                except Exception as e:
                    if package_name in sys.modules:
                        del sys.modules[package_name]
                    raise e

        # Si el archivo no es __init__.py, cargarlo como submódulo
        if file_path.name != "__init__.py":
            module_name = f"{package_name}.{file_path.stem}"
        else:
            module_name = package_name

        spec = importlib.util.spec_from_file_location(
            module_name,
            file_path
        )
        module = importlib.util.module_from_spec(spec)

        # Registrar en sys.modules ANTES de ejecutar para que imports funcionen
        sys.modules[module_name] = module

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            if module_name in sys.modules:
                del sys.modules[module_name]
            raise e
        
        # Buscar clases que hereden de XSalesModule
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, XSalesModule) and 
                attr is not XSalesModule):
                
                # Auto-registrar
                instance = attr()
                metadata = instance.metadata
                
                cls._modules[metadata.name] = attr
                cls._metadata[metadata.name] = metadata
                
                return metadata.name
        
        return None
    
    @classmethod
    def get(cls, name: str) -> XSalesModule:
        """
        Obtiene instancia de submódulo.
        
        Args:
            name: Nombre del módulo
        
        Returns:
            Nueva instancia del módulo
        
        Raises:
            ValueError: Si el módulo no existe
        """
        if not cls._initialized:
            cls.autodiscover()
        
        if name not in cls._modules:
            available = ', '.join(cls._modules.keys())
            raise ValueError(
                f"Módulo '{name}' no encontrado. "
                f"Disponibles: {available}"
            )
        
        return cls._modules[name]()
    
    @classmethod
    def list_modules(cls, enabled_only: bool = True) -> List[ModuleMetadata]:
        """
        Lista submódulos disponibles.
        
        Args:
            enabled_only: Si True, solo módulos habilitados
        
        Returns:
            Lista de metadata de módulos
        """
        if not cls._initialized:
            cls.autodiscover()
        
        modules = list(cls._metadata.values())
        
        if enabled_only:
            modules = [m for m in modules if m.enabled]
        
        return sorted(modules, key=lambda m: m.display_name)
    
    @classmethod
    def get_choices(cls) -> List[str]:
        """
        Obtiene lista de nombres display para menú.
        
        Returns:
            Lista de nombres display
        """
        return [m.display_name for m in cls.list_modules()]
    
    @classmethod
    def exists(cls, name: str) -> bool:
        """
        Verifica si existe un módulo.
        
        Args:
            name: Nombre del módulo
        
        Returns:
            True si existe
        """
        if not cls._initialized:
            cls.autodiscover()
        
        return name in cls._modules


# Instancia global
module_registry = ModuleRegistry()

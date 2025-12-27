"""
Interfaz base para plugins del sistema.
Define el contrato que debe cumplir todo plugin.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class PluginStatus(Enum):
    """Estados posibles de un plugin"""
    UNLOADED = "unloaded"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"


@dataclass
class PluginMetadata:
    """
    Metadata de un plugin.
    Contiene información descriptiva y de configuración.
    """
    name: str
    version: str
    description: str
    author: str
    dependencies: list[str] = field(default_factory=list)
    min_app_version: str = "0.1"
    enabled: bool = True
    
    def __str__(self) -> str:
        return f"{self.name} v{self.version} by {self.author}"


class IPlugin(ABC):
    """
    Interfaz base para todos los plugins del sistema.
    
    Lifecycle de un plugin:
    1. __init__() - Construcción
    2. setup(context) - Inicialización con dependencias
    3. validate() - Validación pre-ejecución
    4. execute() - Ejecución de lógica principal
    5. teardown() - Limpieza de recursos
    
    Ejemplo:
        class MyPlugin(IPlugin):
            @property
            def metadata(self):
                return PluginMetadata(
                    name="myplugin",
                    version="1.0.0",
                    description="Mi plugin personalizado",
                    author="Developer"
                )
            
            def setup(self, context):
                self._context = context
                return True
            
            def execute(self):
                self._context.console.print("Hello from plugin!")
                return {"status": "success"}
            
            def teardown(self):
                pass
            
            def validate(self):
                return True, "OK"
    """
    
    def __init__(self):
        self._status = PluginStatus.UNLOADED
        self._context: Optional['PluginContext'] = None
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """
        Retorna la metadata del plugin.
        Debe ser implementado por cada plugin.
        
        Returns:
            PluginMetadata con información del plugin
        """
        pass
    
    @abstractmethod
    def setup(self, context: 'PluginContext') -> bool:
        """
        Inicialización del plugin con contexto de ejecución.
        
        Se llama una vez antes de execute().
        Usar para:
        - Guardar referencia al contexto
        - Inicializar recursos
        - Configurar dependencias
        - Validar configuración
        
        Args:
            context: Contexto con dependencias inyectadas
        
        Returns:
            True si la inicialización fue exitosa, False en caso contrario
        """
        pass
    
    @abstractmethod
    def execute(self) -> Any:
        """
        Lógica principal del plugin.
        
        Se llama después de setup() exitoso.
        Debe contener toda la funcionalidad del plugin.
        
        Returns:
            Cualquier valor de retorno (resultado de la ejecución)
        """
        pass
    
    @abstractmethod
    def teardown(self) -> None:
        """
        Limpieza de recursos del plugin.
        
        Se llama siempre después de execute(), incluso si hubo error.
        Usar para:
        - Cerrar conexiones
        - Liberar recursos
        - Guardar estado
        - Limpiar archivos temporales
        """
        pass
    
    def validate(self) -> tuple[bool, str]:
        """
        Validación pre-ejecución del plugin.
        
        Se llama antes de execute() para verificar que el plugin
        puede ejecutarse correctamente.
        
        Override para agregar validaciones específicas como:
        - Verificar credenciales
        - Validar archivos requeridos
        - Comprobar conexiones
        - Validar configuración
        
        Returns:
            Tupla (es_valido, mensaje)
            - es_valido: True si puede ejecutarse, False si no
            - mensaje: Descripción del resultado de validación
        """
        return True, "OK"
    
    @property
    def status(self) -> PluginStatus:
        """Retorna el estado actual del plugin"""
        return self._status
    
    @status.setter
    def status(self, value: PluginStatus) -> None:
        """Establece el estado del plugin"""
        self._status = value

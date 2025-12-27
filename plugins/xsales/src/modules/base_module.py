"""
Clase base para submódulos de XSales.
Todos los submódulos (FTP, Server, Status, etc.) heredan de aquí.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ModuleMetadata:
    """
    Metadata de un submódulo de XSales.
    
    Attributes:
        name: Identificador único del módulo (snake_case)
        display_name: Nombre mostrado al usuario
        description: Descripción breve del módulo
        version: Versión del módulo
        author: Autor del módulo
        enabled: Si el módulo está habilitado
    """
    name: str
    display_name: str
    description: str
    version: str = "1.0.0"
    author: str = "PRONACA Team"
    enabled: bool = True
    
    def __str__(self) -> str:
        return f"{self.display_name} ({self.name}) v{self.version}"


class XSalesModule(ABC):
    """
    Clase base abstracta para submódulos de XSales.
    
    Todos los submódulos de XSales (FTP, Server, Status, etc.)
    deben heredar de esta clase e implementar los métodos abstractos.
    
    Lifecycle:
    1. __init__() - Construcción
    2. setup(context) - Inicialización con contexto
    3. validate() - Validación (opcional)
    4. run(context) - Ejecución principal
    5. cleanup() - Limpieza (opcional)
    
    Ejemplo:
        @ModuleRegistry.register
        class MiModulo(XSalesModule):
            @property
            def metadata(self):
                return ModuleMetadata(
                    name="mimodulo",
                    display_name="Mi Módulo",
                    description="Descripción del módulo"
                )
            
            def setup(self, context):
                self._context = context
                return True
            
            def run(self, context):
                context.console.print("Ejecutando...")
                return {"status": "success"}
    """
    
    def __init__(self):
        """Constructor base del módulo"""
        self.config = None
        self.dato = None
        self._context: Optional['PluginContext'] = None
    
    @property
    @abstractmethod
    def metadata(self) -> ModuleMetadata:
        """
        Metadata del submódulo.
        Debe ser implementado por cada submódulo.
        
        Returns:
            ModuleMetadata con información del módulo
        """
        pass
    
    def setup(self, context: 'PluginContext') -> bool:
        """
        Inicialización del submódulo.
        
        Override para configuración específica del módulo.
        Por defecto solo guarda la referencia al contexto.
        
        Args:
            context: Contexto con dependencias inyectadas
        
        Returns:
            True si inicialización exitosa, False si no
        """
        self._context = context
        return True
    
    @abstractmethod
    def run(self, context: 'PluginContext') -> Any:
        """
        Lógica principal del submódulo.
        
        DEBE ser implementado por cada submódulo.
        Contiene toda la funcionalidad del módulo.
        
        Args:
            context: Contexto con dependencias inyectadas
        
        Returns:
            Resultado de la ejecución
        """
        pass
    
    def cleanup(self) -> None:
        """
        Limpieza de recursos del submódulo.
        
        Override si necesitas liberar recursos específicos:
        - Cerrar conexiones
        - Liberar archivos
        - Limpiar datos temporales
        """
        pass
    
    def validate(self) -> tuple[bool, str]:
        """
        Validación antes de ejecutar el módulo.
        
        Override para validaciones específicas:
        - Verificar credenciales
        - Validar configuración
        - Comprobar conexiones
        
        Returns:
            Tupla (es_valido, mensaje)
        """
        return True, "OK"

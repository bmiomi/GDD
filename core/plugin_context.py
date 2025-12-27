"""
Contexto de ejecución para plugins.
Proporciona acceso a dependencias mediante inyección.
"""
from dataclasses import dataclass, field
from typing import Any, Dict
from rich.console import Console
import questionary


@dataclass
class PluginContext:
    """
    Contenedor de dependencias para plugins.
    
    Proporciona acceso centralizado a:
    - Console (rich) para salida formateada
    - Questionary para input interactivo
    - Configuración del plugin
    - Datos compartidos entre plugins
    - Ruta del workspace
    
    Uso en plugin:
        def setup(self, context: PluginContext):
            self._context = context
            self._console = context.console
            config = context.config
            
        def execute(self):
            self._console.print("[green]Hello!")
            answer = self._context.questionary.confirm("Continue?").ask()
    """
    
    console: Console
    questionary: questionary
    config: Dict[str, Any]
    shared_data: Dict[str, Any] = field(default_factory=dict)
    workspace_path: str = ""
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene valor de datos compartidos.
        
        Args:
            key: Clave del dato
            default: Valor por defecto si no existe
        
        Returns:
            Valor almacenado o default
        """
        return self.shared_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Establece valor en datos compartidos.
        
        Args:
            key: Clave del dato
            value: Valor a almacenar
        """
        self.shared_data[key] = value
    
    def has(self, key: str) -> bool:
        """
        Verifica si existe una clave en datos compartidos.
        
        Args:
            key: Clave a verificar
        
        Returns:
            True si existe, False si no
        """
        return key in self.shared_data
    
    def clear_shared_data(self) -> None:
        """Limpia todos los datos compartidos"""
        self.shared_data.clear()

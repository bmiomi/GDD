"""
Inyección de dependencias - Contenedor DI.
"""
from typing import Optional, Type, Callable, Any


class DIContainer:
    """Contenedor simple de inyección de dependencias."""
    
    def __init__(self):
        self._services = {}
    
    def register(self, name: str, factory: Callable[[], Any]):
        """
        Registra una factory para crear servicios.
        
        Args:
            name: Nombre del servicio
            factory: Callable que retorna la instancia
        """
        self._services[name] = {
            'factory': factory,
            'instance': None,
            'is_instance': False,
        }
    
    def register_instance(self, name: str, instance: Any):
        """
        Registra una instancia específica (singleton).
        
        Args:
            name: Nombre del servicio
            instance: Instancia ya creada
        """
        self._services[name] = {
            'factory': None,
            'instance': instance,
            'is_instance': True,
        }
    
    def get(self, name: str) -> Any:
        """
        Obtiene una instancia de un servicio.
        
        Args:
            name: Nombre del servicio
        
        Returns:
            Instancia del servicio
        
        Raises:
            KeyError: Si el servicio no está registrado
        """
        if name not in self._services:
            raise KeyError(f"Servicio no registrado: {name}")
        
        service = self._services[name]
        
        # Si es una instancia directa, devolverla
        if service['is_instance']:
            return service['instance']
        
        # Si ya se creó la instancia de la factory, devolverla (lazy singleton)
        if service['instance'] is not None:
            return service['instance']
        
        # Crear instancia usando la factory
        instance = service['factory']()
        
        # Guardar como singleton (lazy initialization)
        self._services[name]['instance'] = instance
        
        return instance


# Contenedor global (será inicializado desde el módulo)
_container: Optional[DIContainer] = None


def get_di_container() -> DIContainer:
    """Obtiene el contenedor global de DI."""
    global _container
    if _container is None:
        _container = DIContainer()
    return _container


def set_di_container(container: DIContainer):
    """Establece el contenedor global de DI."""
    global _container
    _container = container

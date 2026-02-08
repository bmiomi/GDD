"""
Interfaces genéricas (Puertos) compartidas por todos los plugins.
"""
from abc import ABC, abstractmethod
from core.domain import QueryResult, Preferences


class ResultPresenter(ABC):
    """Puerto para presentar resultados (tabla, lista, resumen, etc)."""
    
    @abstractmethod
    def present(self, result: QueryResult) -> None:
        """Presenta un resultado."""
        pass


class PreferencesRepository(ABC):
    """Puerto para gestionar preferencias persistentes."""
    
    @abstractmethod
    def load(self, module_name: str) -> Preferences:
        """Carga preferencias de un módulo."""
        pass
    
    @abstractmethod
    def save(self, module_name: str, preferences: Preferences) -> bool:
        """Guarda preferencias de un módulo."""
        pass
    
    @abstractmethod
    def exists(self, module_name: str) -> bool:
        """¿Existen preferencias guardadas?"""
        pass


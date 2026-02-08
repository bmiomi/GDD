"""
Repositories (Interfaces) específicas de ServerModule.

Las implementaciones concretas (Yaml, SQLite, etc.) van aquí también.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..domain import Query

# Interfaces
class QueryRepository(ABC):
    """Interface para acceder a consultas."""
    
    @abstractmethod
    def get(self, name: str) -> Query:
        """Obtiene una consulta por nombre."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Query]:
        """Lista todas las consultas."""
        pass
    
    @abstractmethod
    def save(self, query: Query) -> bool:
        """Guarda una consulta."""
        pass
    
    @abstractmethod
    def delete(self, name: str) -> bool:
        """Elimina una consulta."""
        pass


class QueryValidator(ABC):
    """Interface para validar consultas."""
    
    @abstractmethod
    def validate(self, query: Query) -> tuple[bool, str]:
        """Valida una consulta."""
        pass


class QueryExecutor(ABC):
    """Interface para ejecutar consultas."""
    
    @abstractmethod
    def execute(self, query: Query, params: Dict[str, str]) -> 'QueryResult':
        """Ejecuta una consulta con parámetros."""
        pass


# Implementaciones concretas
from .yaml_query_repository import YamlQueryRepository
from .xsales_query_validator import XSalesQueryValidator
from .xsales_query_executor import XSalesQueryExecutor

__all__ = [
    'QueryRepository',
    'QueryValidator',
    'QueryExecutor',
    'YamlQueryRepository',
    'XSalesQueryValidator',
    'XSalesQueryExecutor',
]

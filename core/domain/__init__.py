"""
Domain Layer - Modelos puros genéricos (sin dependencias).
Los modelos específicos van en cada PLUGIN.
"""
from .exceptions import (
    XSalesException,
    QueryExecutionError,
    AuthenticationError,
    ValidationError,
    ConfigurationError,
    QueryNotFoundError,
)
from .query_result import QueryResult
from .preferences import Preferences

__all__ = [
    'XSalesException',
    'QueryExecutionError',
    'AuthenticationError',
    'ValidationError',
    'ConfigurationError',
    'QueryNotFoundError',
    'QueryResult',
    'Preferences',
]

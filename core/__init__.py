"""
Core framework para el sistema de plugins.
Contiene SOLO componentes compartidos (genéricos).
Lógica específica va en PLUGINS.
"""
from .app import MyApplication
from .config_manager import ConfigManager, config_manager

# Domain Layer
from .domain import (
    QueryResult,
    Preferences,
    XSalesException,
    QueryExecutionError,
    AuthenticationError,
    ValidationError,
    ConfigurationError,
    QueryNotFoundError,
)

# Repositories (Interfaces genéricas)
from .repositories import (
    ResultPresenter,
    PreferencesRepository,
)

# DI Container
from .di_container import DIContainer, get_di_container, set_di_container

__all__ = [
    'MyApplication',
    'ConfigManager',
    'config_manager',
    # Domain
    'QueryResult',
    'Preferences',
    'XSalesException',
    'QueryExecutionError',
    'AuthenticationError',
    'ValidationError',
    'ConfigurationError',
    'QueryNotFoundError',
    # Repositories
    'ResultPresenter',
    'PreferencesRepository',
    # DI
    'DIContainer',
    'get_di_container',
    'set_di_container',
]


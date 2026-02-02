"""
Core framework para el sistema de plugins.
"""
from .app import MyApplication
from .config_manager import ConfigManager, config_manager

__all__ = ['MyApplication', 'ConfigManager', 'config_manager']

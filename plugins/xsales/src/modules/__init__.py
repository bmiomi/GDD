# -*- coding: utf-8 -*-
"""
Sistema de submódulos de XSales
"""
from .base_module import XSalesModule, ModuleMetadata
from .module_registry import ModuleRegistry, module_registry

__all__ = [
    'XSalesModule',
    'ModuleMetadata',
    'ModuleRegistry',
    'module_registry',
    'XsalesFactory'
]

# Legacy exports (mantener compatibilidad temporal)
# Solo importar si es necesario para evitar errores de dependencias circulares
try:
    from .FTP import FtpXsales
    from .Status.Status import Status
    from .Server import Page
    
    class XsalesFactory:
        """Factory legacy - mantenido para compatibilidad"""
        
        @classmethod
        def getModulo(cls, value: str) -> object:
            modulo = {'Server': Page, 'Ftp': FtpXsales, 'Status': Status}
            return modulo.get(value, lambda: None)()
except ImportError as e:
    # Los módulos legacy no están disponibles, solo usar nueva arquitectura
    class XsalesFactory:
        """Factory legacy - stub cuando imports fallan"""
        @classmethod
        def getModulo(cls, value: str) -> object:
            return None




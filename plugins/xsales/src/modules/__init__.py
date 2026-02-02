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
    'module_registry'
]




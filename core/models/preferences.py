"""
Preferencias de visualización y salida.
"""
from dataclasses import dataclass
from typing import Literal


@dataclass
class PreferenceData:
    """Preferencias de un submódulo."""
    
    # Formato de salida
    output_format: Literal['table', 'list', 'summary'] = 'table'
    
    # Excel
    generate_excel: bool = False
    open_excel_when_done: bool = False
    
    # Logging
    log_level: Literal['normal', 'debug'] = 'normal'
    show_sql: bool = False
    
    # Almacenamiento
    excel_directory: str = './reports'
    
    def to_dict(self):
        """Convertir a diccionario para guardar en YAML."""
        return {
            'output_format': self.output_format,
            'generate_excel': self.generate_excel,
            'open_excel_when_done': self.open_excel_when_done,
            'log_level': self.log_level,
            'show_sql': self.show_sql,
            'excel_directory': self.excel_directory,
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crear desde diccionario (YAML)."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

"""
Modelo de Preferencias.
"""
from dataclasses import dataclass, asdict
from typing import Literal, Optional


@dataclass
class Preferences:
    """Preferencias de visualización y comportamiento."""
    
    # Formato de salida
    output_format: Literal['tabla', 'lista', 'resumen'] = 'tabla'
    
    # Excel
    generate_excel: bool = False
    open_excel_when_done: bool = False
    excel_directory: str = './REPORTES'
    
    # Logging y debugging
    log_level: Literal['normal', 'debug'] = 'normal'
    show_sql: bool = False
    
    def to_dict(self) -> dict:
        """Convierte a diccionario para guardar en YAML."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Preferences':
        """Crea desde diccionario (ej: del YAML)."""
        # Filtrar solo los campos válidos
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)
    
    @classmethod
    def default(cls) -> 'Preferences':
        """Preferencias por defecto."""
        return cls()

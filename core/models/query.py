"""
Modelo para consultas personalizadas.
"""
from dataclasses import dataclass, field
from typing import List, Optional
import re


@dataclass
class QueryData:
    """Consulta personalizada con parámetros."""
    
    name: str
    sql: str
    parametros_usuario: List[str] = field(default_factory=list)
    descripcion: Optional[str] = None
    
    def validate(self) -> tuple[bool, str]:
        """
        Validar que los placeholders en SQL coincidan con parámetros.
        
        Returns:
            (is_valid, message)
        """
        # Encontrar todos los placeholders {{param}}
        placeholders = set(re.findall(r'\{\{(\w+)\}\}', self.sql))
        params_set = set(self.parametros_usuario)
        
        # Parámetros de sistema que siempre están disponibles
        sistema_params = {'NDISTRIBUIDOR'}
        
        faltantes = placeholders - params_set - sistema_params
        
        if faltantes:
            return False, f"Placeholders sin definir: {', '.join(faltantes)}"
        
        sobran = params_set - placeholders
        if sobran:
            return False, f"Parámetros definidos pero no usados: {', '.join(sobran)}"
        
        return True, "Validación correcta"
    
    def to_dict(self):
        """Convertir a diccionario para guardar en YAML."""
        return {
            'sql': self.sql,
            'parametros_usuario': self.parametros_usuario,
            'descripcion': self.descripcion,
        }
    
    @classmethod
    def from_dict(cls, name: str, data: dict):
        """Crear desde diccionario (YAML)."""
        return cls(
            name=name,
            sql=data.get('sql', ''),
            parametros_usuario=data.get('parametros_usuario', []),
            descripcion=data.get('descripcion')
        )

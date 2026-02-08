"""
Modelo de Consulta (Query).
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from core.domain import ValidationError
import re


@dataclass
class Query:
    """Representa una consulta SQL con parámetros."""
    
    name: str
    sql: str
    parametros_usuario: List[str] = field(default_factory=list)
    parametros_sistema: List[str] = field(default_factory=list)
    descripcion: Optional[str] = None
    sql_condition: Optional[str] = None  # Para SQL condicional: guarda la parte 'if'
    sql_else: Optional[str] = None  # Para SQL condicional: guarda la parte 'else'
    
    def get_all_parameters(self) -> List[str]:
        """Obtiene todos los parámetros (usuario + sistema)."""
        return self.parametros_usuario + self.parametros_sistema
    
    def get_placeholders(self) -> set:
        """Extrae los placeholders {{NOMBRE}} del SQL."""
        # Extraer de la parte SQL principal
        placeholders = set(re.findall(r'\{\{(\w+)\}\}', self.sql))
        
        # Si hay condición SQL, también extraer placeholders de ella
        if self.sql_condition:
            condition_placeholders = set(re.findall(r'\{\{(\w+)\}\}', self.sql_condition))
            placeholders.update(condition_placeholders)

        if self.sql_else:
            else_placeholders = set(re.findall(r'\{\{(\w+)\}\}', self.sql_else))
            placeholders.update(else_placeholders)
        
        return placeholders
    
    def validate(self) -> tuple[bool, str]:
        """
        Valida que la consulta sea consistente.
        
        Returns:
            (is_valid, message)
        """
        if not self.name or not self.name.strip():
            return False, "Nombre de consulta requerido"
        
        if not self.sql or not self.sql.strip():
            return False, "SQL requerido"
        
        placeholders = self.get_placeholders()
        all_params = set(self.get_all_parameters())
        
        # Placeholders que no están definidos
        undefined = placeholders - all_params
        if undefined:
            return False, f"Placeholders sin definir: {', '.join(undefined)}"
        
        # Parámetros definidos pero no usados
        unused = all_params - placeholders
        if unused:
            return False, f"Parámetros sin usar: {', '.join(unused)}"
        
        return True, "Validación correcta"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para guardar en YAML."""
        return {
            'sql': self.sql,
            'parametros_usuario': self.parametros_usuario,
            'parametros_sistema': self.parametros_sistema,
            'descripcion': self.descripcion,
        }
    
    @classmethod
    def from_dict(cls, name: str, data: dict) -> 'Query':
        """Crea desde diccionario (ej: del YAML)."""
        # Procesar SQL (puede ser string o dict condicional)
        sql = data.get('sql', '')
        sql_condition = None
        sql_else = None
        
        if isinstance(sql, dict):
            # SQL condicional: {'if': 'condition', 'then': 'SELECT ...'}
            sql_condition = sql.get('if')
            sql_else = sql.get('else')
            if 'then' in sql:
                sql = sql['then']
            else:
                sql = ''
        
        return cls(
            name=name,
            sql=sql,
            parametros_usuario=data.get('parametros_usuario', []),
            parametros_sistema=data.get('parametros_sistema', []),
            descripcion=data.get('descripcion'),
            sql_condition=sql_condition,
            sql_else=sql_else
        )

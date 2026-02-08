"""
Modelo para resultados de consultas.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ResultData:
    """Datos de resultado de una consulta (sin formato)."""
    
    query_name: str
    columns: List[str] = field(default_factory=list)
    rows: List[Dict[str, Any]] = field(default_factory=list)
    total_rows: int = 0
    execution_time: float = 0.0  # segundos
    error: str = None
    
    def is_success(self) -> bool:
        """¿La consulta fue exitosa?"""
        return self.error is None
    
    def get_summary(self) -> Dict[str, Any]:
        """Información resumida."""
        return {
            'query': self.query_name,
            'total_rows': self.total_rows,
            'execution_time': f"{self.execution_time:.2f}s",
            'status': 'success' if self.is_success() else 'error',
            'error': self.error,
        }

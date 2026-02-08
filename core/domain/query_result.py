"""
Modelo de Resultado de Consulta (QueryResult).
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class QueryResult:
    """Representa el resultado de ejecutar una consulta."""
    
    query_name: str
    columns: List[str] = field(default_factory=list)
    rows: List[Dict[str, Any]] = field(default_factory=list)
    total_rows: int = 0
    execution_time: float = 0.0
    error: Optional[str] = None
    error_details: Optional[str] = None
    
    def is_success(self) -> bool:
        """¿La consulta fue exitosa?"""
        return self.error is None
    
    def is_empty(self) -> bool:
        """¿Resultado sin datos?"""
        return len(self.rows) == 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Información resumida del resultado."""
        return {
            'query': self.query_name,
            'total_rows': self.total_rows,
            'execution_time': f"{self.execution_time:.2f}s",
            'status': 'success' if self.is_success() else 'error',
            'error': self.error,
            'is_empty': self.is_empty(),
        }
    
    def add_row(self, row: Dict[str, Any]) -> None:
        """Agrega una fila al resultado."""
        self.rows.append(row)
        self.total_rows += 1
    
    def add_rows(self, rows: List[Dict[str, Any]]) -> None:
        """Agrega múltiples filas."""
        self.rows.extend(rows)
        self.total_rows = len(self.rows)
    
    def set_error(self, error: str, details: str = None) -> None:
        """Marca resultado como error."""
        self.error = error
        self.error_details = details

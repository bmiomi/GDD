"""
Validador de consultas para ServerModule (XSales).
Valida que SQL sea consistente con parámetros.
"""
from ..domain import Query


class XSalesQueryValidator:
    """Valida consultas XSales específicamente."""
    
    def validate(self, query: Query) -> tuple[bool, str]:
        """
        Valida que la consulta sea consistente.
        
        Args:
            query: Query a validar
        
        Returns:
            (is_valid, message)
        """
        # Delegar a la validación del modelo
        return query.validate()

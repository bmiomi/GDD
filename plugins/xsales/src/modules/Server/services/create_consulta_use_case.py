"""
Use Case: Crear una nueva consulta personalizada (para ServerModule).
"""
from ..domain import Query
from core.domain import ValidationError


class CreateConsultaUseCase:
    """Crea y guarda una nueva consulta personalizada."""
    
    def __init__(self, query_repo: 'QueryRepository'):
        self.query_repo = query_repo
    
    def execute(
        self,
        name: str,
        sql: str,
        parametros_usuario: list,
        parametros_sistema: list = None,
        descripcion: str = None,
    ) -> Query:
        """
        Crea una nueva consulta.
        
        Args:
            name: Nombre de la consulta
            sql: SQL con placeholders {{PARAM}}
            parametros_usuario: Lista de parámetros del usuario
            parametros_sistema: Lista de parámetros del sistema
            descripcion: Descripción opcional
        
        Returns:
            Query creada
        
        Raises:
            ValidationError: Si la consulta no es válida
        """
        parametros_sistema = parametros_sistema or []
        
        query = Query(
            name=name,
            sql=sql,
            parametros_usuario=parametros_usuario,
            parametros_sistema=parametros_sistema,
            descripcion=descripcion,
        )
        
        # Validar
        is_valid, message = query.validate()
        if not is_valid:
            raise ValidationError(
                f"Consulta inválida: {message}",
                field="query"
            )
        
        return query

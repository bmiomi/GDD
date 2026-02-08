"""
Use Case: Ejecutar una consulta (para ServerModule).
"""
from typing import Dict, Any
from ..domain import Query
from core.domain import QueryResult, QueryExecutionError
from core.repositories import ResultPresenter


class RunQueryUseCase:
    """Orquesta la ejecución de una consulta."""
    
    def __init__(
        self,
        query_repo: 'QueryRepository',
        validator: 'QueryValidator',
        executor: 'QueryExecutor',
        presenter: ResultPresenter,
    ):
        self.query_repo = query_repo
        self.validator = validator
        self.executor = executor
        self.presenter = presenter
    
    def execute(self, query_name: str, user_params: Dict[str, str] = None) -> QueryResult:
        """
        Ejecuta una consulta.
        
        Args:
            query_name: Nombre de la consulta
            user_params: Parámetros ingresados por usuario
        
        Returns:
            QueryResult con los datos o error
        
        Raises:
            QueryNotFoundError: Si la consulta no existe
            ValidationError: Si la validación falla
            QueryExecutionError: Si falla la ejecución
        """
        user_params = user_params or {}
        
        try:
            # 1. Obtener consulta
            query = self.query_repo.get(query_name)
            
            # 2. Validar
            is_valid, message = self.validator.validate(query)
            if not is_valid:
                raise QueryExecutionError(
                    f"Validación fallida: {message}",
                    query_name=query_name
                )
            
            # 3. Ejecutar
            result = self.executor.execute(query, user_params)
            
            # 4. Presentar
            self.presenter.present(result)
            
            return result
            
        except QueryExecutionError:
            raise
        except Exception as e:
            raise QueryExecutionError(
                f"Error ejecutando consulta: {str(e)}",
                query_name=query_name,
                details=str(e)
            )

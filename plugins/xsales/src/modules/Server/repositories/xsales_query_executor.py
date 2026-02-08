"""
Ejecutor de consultas para ServerModule.
Ejecuta queries contra el servidor XSales usando XSalesHttpClient.
"""
from typing import Dict
import logging
import time
from ..domain import Query
from ..infrastructure import XSalesHttpClient
from core.domain import QueryResult, QueryExecutionError


logger = logging.getLogger(__name__)


class XSalesQueryExecutor:
    """Ejecuta consultas contra XSales."""
    
    def __init__(self, http_client: XSalesHttpClient = None):
        """
        Args:
            http_client: Cliente HTTP de XSales (opcional para testing)
        """
        self.http_client = http_client
    
    def execute(self, query: Query, params: Dict[str, str]) -> QueryResult:
        """
        Ejecuta una consulta en XSales.
        
        Args:
            query: Query a ejecutar
            params: Parámetros del usuario + sistema
        
        Returns:
            QueryResult con los datos
        
        Raises:
            QueryExecutionError: Si falla
        """
        try:
            # 1. Determinar SQL correcta según condición (si aplica)
            sql = self._resolve_conditional_sql(query, params)
            
            # 2. Sustituir parámetros en el SQL
            sql = self._substitute_params(sql, params)
            
            logger.info(f"Ejecutando query '{query.name}'")
            logger.debug(f"SQL: {sql[:200]}...")
            
            # 3. Ejecutar en XSales
            if not self.http_client:
                raise QueryExecutionError(
                    "No hay cliente HTTP configurado",
                    query_name=query.name
                )
            
            start_time = time.time()
            response = self.http_client.execute_query(sql)
            execution_time = time.time() - start_time
            
            # 4. Verificar si hubo error
            if not response.get('success'):
                return QueryResult(
                    query_name=query.name,
                    columns=[],
                    rows=[],
                    total_rows=0,
                    execution_time=execution_time,
                    error=response.get('error', 'Error desconocido')
                )
            
            # 5. Construir QueryResult exitoso
            data = response.get('data', [])
            return QueryResult(
                query_name=query.name,
                columns=response.get('columns', []),
                rows=data,
                total_rows=len(data),
                execution_time=execution_time,
            )
            
        except Exception as e:
            logger.error(f"Error ejecutando '{query.name}': {e}")
            raise QueryExecutionError(
                f"Error ejecutando consulta: {str(e)}",
                query_name=query.name,
                details=str(e),
            )
    
    def _resolve_conditional_sql(self, query: Query, params: Dict[str, str]) -> str:
        """
        Resuelve SQL condicional según la condición 'if'.
        
        Si la query tiene SQL condicional (if/then/else), evalúa la condición
        y devuelve el SQL correspondiente.
        
        Args:
            query: Query con posible SQL condicional
            params: Parámetros para evaluar condición
        
        Returns:
            SQL a ejecutar (then o else)
        """
        # Si no hay SQL condicional, devolver SQL simple
        if not query.sql_condition:
            return query.sql
        
        # Evaluar condición con parámetros
        if self._evaluate_condition(query.sql_condition, params):
            return query.sql  # 'then'
        else:
            if query.sql_else:
                return query.sql_else
            logger.warning(
                f"Consulta '{query.name}' no tiene SQL 'else' para condicion false"
            )
            return ""
    
    def _evaluate_condition(self, condition: str, params: Dict[str, str]) -> bool:
        """
        Evalúa una condición booleana reemplazando placeholders.
        
        Ejemplo:
            condition = "{{NDISTRIBUIDOR}} == 'PRONACA'"
            params = {'NDISTRIBUIDOR': 'PRONACA'}
            → True
            
            condition = "{{NDISTRIBUIDOR}} == 'PRONACA'"
            params = {'NDISTRIBUIDOR': 'CENACOP'}
            → False
        
        Args:
            condition: Condición con placeholders
            params: Parámetros a reemplazar
        
        Returns:
            Resultado de la evaluación
        """
        import re
        
        # Reemplazar placeholders {{PARAM}} con valores
        evaluated = condition
        for key, value in params.items():
            placeholder = f"{{{{{key}}}}}"
            # Agregar comillas si el valor es string
            replacement = f"'{value}'" if isinstance(value, str) else str(value)
            evaluated = evaluated.replace(placeholder, replacement)
        
        logger.debug(f"Evaluando condición: {condition}")
        logger.debug(f"Después de reemplazos: {evaluated}")
        
        try:
            # Evaluar la expresión de forma segura
            result = eval(evaluated, {"__builtins__": {}})
            logger.debug(f"Resultado: {result}")
            return bool(result)
        except Exception as e:
            logger.error(f"Error evaluando condición '{condition}': {e}")
            return False
    
    def _substitute_params(self, sql: str, params: Dict[str, str]) -> str:
        """
        Sustituye placeholders {{PARAM}} en el SQL.
        
        Args:
            sql: SQL con placeholders
            params: Diccionario de parámetros
        
        Returns:
            SQL con parámetros sustituidos
        """
        result = sql
        for key, value in params.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        return result

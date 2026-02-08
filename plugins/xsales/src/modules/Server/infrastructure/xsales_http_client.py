"""
Cliente HTTP para XSales - Versión inyectable y testeable.
Envuelve la lógica de autenticación y consultas de xsalesbeta.py
"""
import logging
from typing import Optional, Dict, Any, List
from plugins.xsales.src.modules.Server.Pagedriver.xsalesbeta import Xsales
from core.domain import QueryExecutionError, AuthenticationError

logger = logging.getLogger(__name__)


class XSalesHttpClient:
    """Cliente HTTP para interactuar con el servidor XSales."""
    
    def __init__(self, distributor_name: str):
        """
        Args:
            distributor_name: Nombre del distribuidor (tenant)
        """
        self.distributor_name = distributor_name
        self._xsales: Optional[Xsales] = None
        self._initialized = False
    
    def _ensure_connection(self):
        """Asegura que la conexión esté inicializada."""
        if not self._initialized:
            try:
                self._xsales = Xsales(name=self.distributor_name)
                if not hasattr(self._xsales, 'estado') or not self._xsales.estado:
                    raise AuthenticationError(
                        f"No se pudo autenticar con {self.distributor_name}",
                        server=self.distributor_name
                    )
                self._initialized = True
                logger.info(f"✓ Cliente XSales inicializado para {self.distributor_name}")
            except Exception as e:
                logger.error(f"✗ Error inicializando XSales para {self.distributor_name}: {e}")
                raise AuthenticationError(
                    f"Error de autenticación: {str(e)}",
                    server=self.distributor_name
                )
    
    def execute_query(self, sql: str) -> Dict[str, Any]:
        """
        Ejecuta una consulta SQL en el servidor XSales.
        
        Args:
            sql: Query SQL a ejecutar
        
        Returns:
            Diccionario con la respuesta:
            {
                'success': bool,
                'data': List[Dict],  # Filas del resultado
                'columns': List[str],
                'error': Optional[str]
            }
        
        Raises:
            AuthenticationError: Si no puede autenticarse
            QueryExecutionError: Si la query falla
        """
        self._ensure_connection()
        
        try:
            logger.debug(f"Ejecutando query en {self.distributor_name}")
            logger.debug(f"SQL: {sql[:200]}...")
            
            # Ejecutar consulta
            result = self._xsales.consultar(sql)
            
            # Procesar respuesta
            if getattr(self._xsales, 'use_query_api', False) and self._xsales.xsalesresponse_json:
                return self._parse_json_response(self._xsales.xsalesresponse_json)
            elif isinstance(result, list):
                return self._parse_list_response(result)
            else:
                logger.warning(f"Respuesta inesperada de XSales: {type(result)}")
                return {
                    'success': False,
                    'data': [],
                    'columns': [],
                    'error': 'Formato de respuesta desconocido'
                }
        
        except Exception as e:
            logger.error(f"Error ejecutando query: {e}")
            raise QueryExecutionError(
                message=f"Error ejecutando consulta: {str(e)}",
                query_name="runtime",
                details=str(e)
            )
    
    def _parse_json_response(self, response: Dict) -> Dict[str, Any]:
        """Parsea respuesta JSON de la API de XSales."""
        message_type = response.get('MessageType')
        message = response.get('Message', '')
        
        # MessageType 69 indica error
        if message_type == 69:
            error_msg = message
            
            # Intentar obtener mensaje más específico
            data = response.get('Data')
            if isinstance(data, dict):
                query_inf = data.get('QueryInfResult')
                if isinstance(query_inf, list) and query_inf:
                    error_msg = query_inf[0].get('Msg', message)
            
            return {
                'success': False,
                'data': [],
                'columns': [],
                'error': error_msg
            }
        
        # Extraer datos si no hay error
        data = response.get('Data') if isinstance(response, dict) else None
        dataset = []
        
        if isinstance(data, list):
            dataset = data
        elif isinstance(data, dict):
            result = data.get('Result') or data.get('result') or data.get('data')
            if isinstance(result, list):
                dataset = result
        
        if dataset:
            columns = list(dataset[0].keys()) if dataset and isinstance(dataset[0], dict) else []
            return {
                'success': True,
                'data': dataset,
                'columns': columns,
                'error': None
            }
        
        return {
            'success': True,
            'data': [],
            'columns': [],
            'error': None
        }
    
    def _parse_list_response(self, result: List) -> Dict[str, Any]:
        """Parsea respuesta tipo lista."""
        if result:
            columns = list(result[0].keys()) if result and isinstance(result[0], dict) else []
            return {
                'success': True,
                'data': result,
                'columns': columns,
                'error': None
            }
        
        return {
            'success': True,
            'data': [],
            'columns': [],
            'error': None
        }
    
    def close(self):
        """Cierra la conexión (cleanup)."""
        self._xsales = None
        self._initialized = False

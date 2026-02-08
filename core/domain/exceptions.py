"""
Excepciones personalizadas del dominio.
"""


class XSalesException(Exception):
    """Excepción base del sistema XSales."""
    pass


class QueryExecutionError(XSalesException):
    """Error al ejecutar una consulta SQL."""
    
    def __init__(self, message: str, query_name: str = None, details: str = None):
        self.query_name = query_name
        self.details = details
        super().__init__(message)


class AuthenticationError(XSalesException):
    """Error de autenticación con XSales."""
    
    def __init__(self, message: str, server: str = None):
        self.server = server
        super().__init__(message)


class ValidationError(XSalesException):
    """Error de validación de datos."""
    
    def __init__(self, message: str, field: str = None, value: str = None):
        self.field = field
        self.value = value
        super().__init__(message)


class ConfigurationError(XSalesException):
    """Error en la configuración del sistema."""
    
    def __init__(self, message: str, config_key: str = None):
        self.config_key = config_key
        super().__init__(message)


class QueryNotFoundError(XSalesException):
    """Consulta no encontrada."""
    
    def __init__(self, query_name: str):
        self.query_name = query_name
        super().__init__(f"Consulta no encontrada: {query_name}")

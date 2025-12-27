"""
Gestor de configuración centralizado con soporte para variables de entorno.
Utiliza python-dotenv para cargar credenciales desde archivo .env
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv


class ConfigManager:
    """
    Gestor centralizado de configuración con soporte para variables de entorno.
    
    Características:
    - Carga automática de .env
    - Interpolación de variables ${VAR_NAME}
    - Caché de valores
    - Validación de variables requeridas
    """
    
    _instance: Optional['ConfigManager'] = None
    _env_loaded = False
    
    def __new__(cls):
        """Singleton pattern para garantizar una sola instancia"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Inicializa el gestor de configuración.
        
        Args:
            base_path: Ruta base del proyecto (por defecto: directorio actual)
        """
        if not hasattr(self, 'initialized'):
            self.base_path = base_path or Path.cwd()
            self._cache: Dict[str, Any] = {}
            self._load_env()
            self.initialized = True
    
    def _load_env(self):
        """Carga variables de entorno desde archivo .env"""
        if not ConfigManager._env_loaded:
            env_file = self.base_path / '.env'
            
            if env_file.exists():
                load_dotenv(env_file)
                ConfigManager._env_loaded = True
            else:
                # Intentar cargar desde directorio padre
                parent_env = self.base_path.parent / '.env'
                if parent_env.exists():
                    load_dotenv(parent_env)
                    ConfigManager._env_loaded = True
    
    def get(self, key: str, default: Any = None, required: bool = False) -> Any:
        """
        Obtiene un valor de configuración de las variables de entorno.
        
        Args:
            key: Nombre de la variable (se convierte a mayúsculas automáticamente)
            default: Valor por defecto si no existe
            required: Si True, lanza excepción si la variable no existe
        
        Returns:
            Valor de la variable de entorno
        
        Raises:
            ValueError: Si required=True y la variable no existe
        """
        # Normalizar key a mayúsculas
        key_upper = key.upper()
        
        # Verificar caché
        if key_upper in self._cache:
            return self._cache[key_upper]
        
        # Obtener de environment
        value = os.getenv(key_upper, default)
        
        if required and value is None:
            raise ValueError(
                f"Variable de entorno requerida no encontrada: {key_upper}\n"
                f"Asegúrate de definirla en el archivo .env"
            )
        
        # Cachear valor
        if value is not None:
            self._cache[key_upper] = value
        
        return value
    
    def get_credential(self, service: str, entity: str) -> tuple[str, str]:
        """
        Obtiene credenciales (usuario y contraseña) desde variables de entorno.
        
        Args:
            service: Nombre del servicio (FTP, SERVER, etc.)
            entity: Nombre de la entidad (PRONACA, CENACOP, etc.)
        
        Returns:
            Tupla (usuario, contraseña)
        
        Raises:
            ValueError: Si las credenciales no están definidas
        
        Example:
            >>> config = ConfigManager()
            >>> user, password = config.get_credential('FTP', 'PRONACA')
        """
        service = service.upper()
        entity = entity.upper()
        
        user_key = f'{service}_{entity}_USER'
        pass_key = f'{service}_{entity}_PASS'
        
        user = self.get(user_key)
        password = self.get(pass_key)
        
        if not user or not password:
            raise ValueError(
                f"Credenciales no encontradas para {entity} en servicio {service}.\n"
                f"Asegúrate de definir {user_key} y {pass_key} en el archivo .env\n"
                f"Puedes usar .env.example como referencia."
            )
        
        return (user, password)
    
    def get_ftp_config(self) -> Dict[str, Any]:
        """
        Obtiene configuración completa de FTP.
        
        Returns:
            Diccionario con configuración FTP
        """
        return {
            'host': self.get('FTP_HOST', required=True),
            'port': int(self.get('FTP_PORT', default='990')),
            'protocol': self.get('FTP_PROTOCOL', default='FTPS'),
            'path_download': self.get('FTP_PATH_DOWNLOAD', default='/COMUNES')
        }
    
    def get_server_default_credentials(self) -> tuple[str, str]:
        """
        Obtiene credenciales por defecto del servidor XSales.
        
        Returns:
            Tupla (usuario, contraseña)
        """
        user = self.get('SERVER_DEFAULT_USER', required=True)
        password = self.get('SERVER_DEFAULT_PASS', required=True)
        return (user, password)
    
    def list_available_distributors(self, service: str = 'FTP') -> list[str]:
        """
        Lista distribuidores disponibles según las variables de entorno.
        
        Args:
            service: Servicio a verificar (FTP, SERVER, etc.)
        
        Returns:
            Lista de nombres de distribuidores configurados
        """
        service = service.upper()
        distributors = []
        prefix = f'{service}_'
        suffix = '_USER'
        
        for key in os.environ:
            if key.startswith(prefix) and key.endswith(suffix):
                # Extraer nombre del distribuidor
                distributor = key[len(prefix):-len(suffix)]
                distributors.append(distributor)
        
        return sorted(distributors)
    
    def validate_required_credentials(self, distributors: list[str], service: str = 'FTP'):
        """
        Valida que existan credenciales para una lista de distribuidores.
        
        Args:
            distributors: Lista de nombres de distribuidores
            service: Servicio a validar (FTP, SERVER, etc.)
        
        Raises:
            ValueError: Si faltan credenciales para algún distribuidor
        """
        missing = []
        
        for distributor in distributors:
            try:
                self.get_credential(service, distributor)
            except ValueError:
                missing.append(distributor)
        
        if missing:
            raise ValueError(
                f"Faltan credenciales para los siguientes distribuidores:\n"
                f"{', '.join(missing)}\n"
                f"Por favor, configúralas en el archivo .env"
            )
    
    def clear_cache(self):
        """Limpia el caché de configuración"""
        self._cache.clear()
    
    @staticmethod
    def reload_env():
        """Recarga las variables de entorno desde el archivo .env"""
        ConfigManager._env_loaded = False
        instance = ConfigManager()
        instance._load_env()
        instance.clear_cache()


# Instancia global para facilitar el uso
config_manager = ConfigManager()

from plugins.xsales.src.config import Config

class ConfigFtp(Config):
    """
    Configuración específica del módulo FTP.
    Autocontenida - maneja sus propias credenciales y configuración.
    """

    __user = None
    __operacion = None
    spinner = 'smiley'

    @property
    def configftp(self):
        return self.config.get('datos', {}).get('FTP', {})

    @property
    def operacion(self)->str:
        return self.__operacion

    @operacion.setter
    def operacion(self, value):
        self.__operacion = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    @property
    def protocol(self):
        """Obtiene protocolo desde config o .env"""
        if self.__operacion == "Validar Maestros":
            return self.configftp.get('Maestros', {}).get(self.__user, {}).get('protocol')
        from core.config_manager import config_manager
        return config_manager.get('FTP_PROTOCOL', default='FTPS')

    @property
    def host(self):
        """Obtiene host desde variables de entorno"""
        from core.config_manager import config_manager
        return config_manager.get('FTP_HOST', required=True)

    @property
    def port(self):
        """Obtiene puerto desde variables de entorno"""
        from core.config_manager import config_manager
        return int(config_manager.get('FTP_PORT', default='990'))

    @property
    def pathdownload(self):
        """Obtiene ruta de descarga desde .env o config"""
        path_config = self.configftp.get('Repositorio', {}).get('credenciales', {}).get(self.user, {}).get('path')
        if path_config:
            return path_config.get('Download')
        return config_manager.get('FTP_PATH_DOWNLOAD', default='/COMUNES')

    @property
    def excluide(self):
        """Obtiene lista de archivos excluidos"""
        path = self.configftp.get('Repositorio', {}).get('credenciales', {}).get(self.user, {}).get('excluide')
        if path:
            return path
        return self.configftp.get('excluide', [])

    @property
    def xmlfile(self):
        return self.configftp.get('xmlfile')

    @property
    def CredencialesFtp(self) -> tuple:
        """
        Obtiene credenciales FTP desde variables de entorno.
        
        Returns:
            Tupla (usuario, contraseña)
        """
        if self.__operacion and 'Maestros' in self.__operacion:
            # Para maestros, usar configuración antigua si existe
            credenciales = self.configftp.get('Maestros', {}).get(self.__user, {})
            if credenciales:
                return (credenciales.get('USER'), credenciales.get('PASS'))
        
        # Usar variables de entorno
        try:
            return config_manager.get_credential('FTP', self.__user)
        except ValueError as e:
            # Fallback a config.yml si no existe en .env (para migración gradual)
            credenciales = self.configftp.get('Repositorio', {}).get('credenciales', {}).get(self.__user, {})
            if credenciales:
                return (credenciales.get('USER'), credenciales.get('PASS'))
            raise e

    @property
    def pathdistribudor(self):
        self.nuevacarpeta(self.config.get('PathFolder').get('Distribuidores'),
                      self.user,
                      self.fecha,)
        return self.config.get('PathFolder').get('Distribuidores')

    @property
    def tablevalidacion(self):
       return  self.configftp.get('Validacionfile', {}).get('sqlite', [])

    @property
    def downloadfilebaseruta(self):
       return  self.configftp.get('Repositorio', {}).get('Download', {}).get('file')

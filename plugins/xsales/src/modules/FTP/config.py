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
        """Obtiene protocolo desde config.yml"""
        if self.__operacion == "Validar Maestros":
            return self.configftp.get('Maestros', {}).get(self.__user, {}).get('protocol')
        return self.configftp.get('Repositorio', {}).get('protocol', 'FTPS')

    @property
    def host(self):
        """Obtiene host desde config.yml"""
        return self.configftp.get('Repositorio', {}).get('host', 'prd1.xsalesmobile.net')

    @property
    def port(self):
        """Obtiene puerto desde config.yml"""
        return int(self.configftp.get('Repositorio', {}).get('port', 990))

    @property
    def pathdownload(self):
        """Obtiene ruta de descarga desde config.yml"""
        path_config = self.configftp.get('Repositorio', {}).get('credenciales', {}).get(self.user, {}).get('path')
        if path_config:
            return path_config.get('Download')
        return self.configftp.get('Repositorio', {}).get('Download', {}).get('path', '/COMUNES')

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
        Obtiene credenciales FTP desde config.yml.
        
        Returns:
            Tupla (usuario, contraseña)
        """
        if self.__operacion and 'Maestros' in self.__operacion:
            # Para maestros, usar configuración antigua si existe
            credenciales = self.configftp.get('Maestros', {}).get(self.__user, {})
            if credenciales:
                return (credenciales.get('USER'), credenciales.get('PASS'))
        
        # Usar configuración de config.yml
        credenciales = self.configftp.get('Repositorio', {}).get('credenciales', {}).get(self.__user, {})
        if credenciales:
            return (credenciales.get('USER'), credenciales.get('PASS'))
        return (None, None)

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
    @property
    def configConsultasStructured(self) -> dict:
        """Retorna opciones de FTP como estructura de consultas para el menú"""
        # FTP no tiene SQL, en su lugar usa las opciones del menú (Revisiones.Ftp)
        opciones = self.Revisiones  # Obtiene la lista configurada en Revisiones.Ftp
        
        # Convertir opciones a estructura de diccionario {opcion: {sql: {...}}}
        result = {}
        if isinstance(opciones, list):
            for opcion in opciones:
                result[opcion] = {'sql': {}, 'parametros': []}
        return result
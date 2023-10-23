from plugins.xsales.config import Config

class ConfigFtp(Config):

    __user = None
    __operacion = None
    spinner = 'smiley'

    @property
    def operacion(self):
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
        if self.__operacion == "Validar Maestros":
            return self.config.get('FTP').get('Maestros').get(self.__user).get('protocol')
        return self.config.get('FTP').get('Repositorio').get('protocol')

    @property
    def host(self):
        return self.config.get('FTP').get('Repositorio').get('host')

    @property
    def port(self):
        return self.config.get('FTP').get('Repositorio').get('port')

    @property
    def pathdownload(self):

        path = self.config.get('FTP').get('Repositorio').get(
            'credenciales').get(self.user).get('path', None)
        if path:
            return path.get('Download')
        return self.config.get('FTP').get('defaul_path').get('Download')

    @property
    def excluide(self):
        path = self.config.get('FTP').get('Repositorio').get(
            'credenciales').get(self.user).get('excluide')
        if path:
            return path
        return self.config.get('FTP').get('excluide')

    @property
    def xmlfile(self):
        return self.config.get('FTP').get('xmlfile')

    @property
    def CredencialesFtp(self) -> tuple:
        credenciales = None
        print('se imprime operacion',self.__operacion)
        if 'DESC' in self.__operacion:
            credenciales = self.config.get('FTP').get(
                'Repositorio').get('credenciales').get(self.__user)
        if 'Maestros' in self.__operacion:
            credenciales = self.config.get('FTP').get(
                'Maestros').get(self.__user)
        return self.Credenciales(credenciales)

    def Credenciales(self, credenciales):
        user, password = credenciales.get('USER'), credenciales.get('PASS')
        return (user, password)

    @property
    def pathdistribudor(self):
        return self.config.get('PathFolder').get('Distribuidores')

    def Credenciales(self, credenciales):
        user, password = credenciales.get('USER'), credenciales.get('PASS')
        return (user, password)

    @property
    def pathdistribudor(self):
        createfolder (self.config.get('PathFolder').get('Distribuidores'),
                      self.config.user,
                      self.config.fecha,)
        return self.config.get('PathFolder').get('Distribuidores')


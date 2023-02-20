from datetime import datetime
from typing import Dict
import pandas as pd
import yaml

from .util import createfolder, path, remove, sep, listdir


class Config:

    @property
    def config(self) -> Dict:
        file = path.join(f'plugins{sep}xsales{sep}config.yaml')
        try:
            return yaml.load(
                open(file, 'r'), Loader=yaml.FullLoader)
        except FileNotFoundError:
            print('No se tiene archivo de configuracion.')
            exit()

    @property
    def fecha(self):
        return datetime.today().strftime("%Y-%m-%d")

    @property
    def path(self):
        return path

    def nuevacarpeta(self, *path):
        return createfolder(*path)

    def Dz(self, ldz: dict = {'Opcion': 'TODOS'}) -> list[str]:
        returndz = {
            'TODOS': self.config['FTP']['Repositorio']['credenciales'].keys(),
            'Grupos': [
                {
                    'TECNICO 3-AM':
                    ['PRONACA', 'CENACOP', 'DISPROLOP', 'DISPROALZA', 'MADELI',
                     'PAUL_FLORENCIA', 'POSSO_CUEVA', 'DISPROVALLES']
                },

                {
                    'TECNICO(1) 4-AM':
                    ['JUDISPRO', 'ALMABI', 'DISMAG', 'GRAMPIR',
                     'GARVELPRODUCT', 'DISANAHISA', 'ALSODI', 'PROORIENTE']
                },

                {
                    'TECNICO(2) 4-AM':
                    ['DIMMIA', 'SKANDINAR', 'PRONACNOR', 'APRONAM',
                     'DISCARNICOS', 'ECOAL', 'H_M', 'PATRICIO_CEVALLOS']
                }

            ]
        }
        if ldz.get('Opcion') in ('REVICION_MADRUGADA', 'Validar DESC'):

            return [i for i in map(lambda y: y.get(ldz['Turno']),
                                   map(lambda x: x, returndz.get('Grupos'))) if i
                    ][0]

        if ldz.get('Opcion') == 'Total_Pedidos':
            return returndz.get('TODOS')

        if ldz.get('Opcion') != 'REVICION_MADRUGADA':
            return returndz.get('TODOS')


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
        # createfolder (self.config.get('PathFolder').get('Distribuidores'),
        #               self.config.user,
        #               self.config.fecha,)
        return self.config.get('PathFolder').get('Distribuidores')


class ConfigServer(Config):

    spinner = 'bouncingBall'

    def CredencialesServer(self, credencial='default') -> tuple:
        credenciales = self.config.get('Server').get('credenciales')
        for opcion in credenciales:
            if opcion.get(credencial):
                return opcion[credencial]['USER'], opcion[credencial]['PASSWORD']

    def folderexcel(self) -> str:

        currpath = path.join(
            self.config.get('PathFolder').get('folder_file_excel'),
            self.fecha
        )

        if not path.isdir(currpath):
            createfolder(currpath)
        return currpath+sep

    def folderMadrugada(self) -> str:
        foldermadrugada = self.config.get('PathFolder').get('folderMadrugada')
        if not path.isdir(foldermadrugada):
            createfolder(foldermadrugada)
        return foldermadrugada

    def excelfile(self):
        return ExcelFile


class ConfigStatus(Config):

    spinner = 'monkey'

    @property
    def filestatus(self):
        folder = self.config.get('PathFolder').get('folderStatus')
        path = createfolder(folder)
        return path


class ConfigFactory:

    @classmethod
    def getModulo(cls, value: str = None) -> object:
        if value == 'Server':
            return ConfigServer()
        if value == 'FTP':
            return ConfigFtp()
        if value == 'Status':
            return ConfigStatus()

class ExcelFile:

    """
        Clase  en donde  se procesan y generan archivos de Excel

    """

    _nombrearchivo = f"reporte{ Config().fecha}.xlsx"

    @classmethod
    def excelfile(cls):
        """

        si el archivo exite  validar que la fecha sea igual a la actual.
        si el archivo no exite crear un archivo

        """

        d = datetime.today().date().strftime('%d/%m/%Y')
        c = datetime.fromtimestamp(path.getmtime(
            cls._nombrearchivo)).strftime('%d/%m/%Y')

        if c != d:
            print('\n removiendo el archivo')
            remove(cls._nombrearchivo)

    @classmethod
    def recorrer_tabla(cls, data: str, converts={'Codigo_Cliente': str, 'Id_Negociacion': str}) -> pd.DataFrame:
        return pd.DataFrame(pd.read_html(data, converters=converts)[0]).to_dict('records')

    @classmethod
    def append_df_to_excel(cls, dfs):

        df = pd.DataFrame(dfs)
        if not path.isfile(cls._nombrearchivo):
            df.to_excel(cls._nombrearchivo, index=False)
        else:
            df_excel = pd.read_excel(cls._nombrearchivo, dtype='str')
            result = pd.concat([df_excel, df], ignore_index=True)
            result.to_excel(cls._nombrearchivo, index=False, sheet_name='GDD')

    @classmethod
    def consolidararchivo(cls):
        pathexcel = path.join(ConfigServer().folderexcel())
        r = listdir(pathexcel)
        t = path.abspath(pathexcel)
        for i in range(len(r)):
            directorio = t+'\\'+r[i]
            q = pd.read_excel(directorio, dtype='str')
            cls.append_df_to_excel(q)

    @classmethod
    def filetxt(cls, namearchivo: str, data: dict):
        archiv = ''.join([namearchivo, Config().fecha])
        with open(archiv, 'a') as file:
            for key, value in data.items():
                file.writelines(f'{key} - {value}\n')

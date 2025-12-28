
from plugins.xsales.src.service.excelservice.service_excel import ExcelFile
from plugins.xsales.confi import Config
from plugins.xsales.util import sep

class ConfigServer(Config):

    spinner = 'bouncingBall'

    def CredencialesServer(self, credencial='default') -> tuple:
        credenciales = self.config.get('datod', {}).get('Server', {}).get('credenciales', [])
        for opcion in credenciales:
            if opcion.get(credencial):
                return opcion[credencial]['USER'], opcion[credencial]['PASSWORD']

    def folderexcel(self) -> str:

        currpath = self.path.join(
            self.config.get('PathFolder').get('folder_file_excel'),
            self.fecha
        )

        if not self.path.isdir(currpath):
            self.nuevacarpeta(currpath)
        return currpath+sep

    def folderMadrugada(self) -> str:
        foldermadrugada = self.config.get('PathFolder').get('folderMadrugada')
        if not self.path.isdir(foldermadrugada):
            self.nuevacarpeta(foldermadrugada)
        return foldermadrugada

    def excelfile(self):
        return ExcelFile


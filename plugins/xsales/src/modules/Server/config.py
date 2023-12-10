
from ...config import Config 
from ...Services.excel_services import ExcelFile
from ...util import  path, sep,createfolder

class ConfigServer(Config):

    spinner = 'bouncingBall'

    def CredencialesServer(self, credencial='default') -> tuple:
        credenciales = self.config.get('Server').get('credenciales')
        for opcion in credenciales:
            if opcion.get(credencial):
                return opcion[credencial]['USER'], opcion[credencial]['PASSWORD']
    @property
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


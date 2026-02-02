
from plugins.xsales.src.service.excelservice.service_excel import ExcelFile
from plugins.xsales.src.config import Config
from plugins.xsales.util import sep

class ConfigServer(Config):

    spinner = 'bouncingBall'

    def CredencialesServer(self, credencial='default') -> tuple:
        config_data = self.config
        datod = config_data.get('datod', {})
        print("Se Obtuvo CredencialesServer", credencial)
        if not isinstance(datod, dict):
            raise TypeError(f"'datod' should be dict but is {type(datod)}")
        
        server = datod.get('Server', {})
        
        if not isinstance(server, dict):
            raise TypeError(f"'Server' should be dict but is {type(server)}")
        
        credenciales = server.get('credenciales', [])
        
        for opcion in credenciales:
            if opcion.get(credencial):
                print(f"Credenciales obtenidas para {credencial } ")
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

    @property
    def configConsultas(self) -> dict:
        """Retorna la configuración de consultas desde config.yml"""
        config_data = self.config
        datod = config_data.get('datod', {})
        server = datod.get('Server', {})
        return server.get('Consultas', {})
    
    @property
    def configConsultasStructured(self) -> dict:
        """Retorna consultas estructuradas para usar con consultas.consulta()"""
        consultas_raw = self.configConsultas
        # Convertir cada consulta a la estructura esperada por consultas.consulta()
        # Transforma: {'REVICION_MADRUGADA': {'sql': {...}}} 
        # A: {'REVICION_MADRUGADA': {'sql': {...}, 'parametros': [...]}}
        result = {}
        for key, value in consultas_raw.items():
            if isinstance(value, dict) and 'sql' in value:
                result[key] = value
            else:
                # Si no tiene estructura correcta, envolver en 'sql'
                result[key] = {'sql': value, 'parametros': []}
        return result

    def excelfile(self):
        return ExcelFile


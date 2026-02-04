
from plugins.xsales.src.config import Config

class ConfigStatus(Config):

    spinner = 'monkey'

    @property
    def filestatus(self):
        folder = self.config.get('PathFolder').get('folderStatus')
        return self.nuevacarpeta(folder)

    @property
    def configConsultasStructured(self) -> dict:
        """Retorna opciones de Status como estructura de consultas para el menú"""
        # Status no tiene SQL, en su lugar usa las opciones del menú (Revisiones.Status)
        opciones = self.Revisiones  # Obtiene la lista configurada en Revisiones.Status
        
        # Convertir opciones a estructura de diccionario {opcion: {sql: {...}}}
        result = {}
        if isinstance(opciones, list):
            for opcion in opciones:
                result[opcion] = {'sql': {}, 'parametros': []}
        return result


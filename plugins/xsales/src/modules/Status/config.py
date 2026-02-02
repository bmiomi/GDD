
from plugins.xsales.src.config import Config

class ConfigStatus(Config):

    spinner = 'monkey'

    @property
    def filestatus(self):
        folder = self.config.get('PathFolder').get('folderStatus')
        return self.nuevacarpeta(folder)


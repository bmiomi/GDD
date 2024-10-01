
from plugins.xsales.confi import Config

class ConfigStatus(Config):

    spinner = 'monkey'

    @property
    def filestatus(self):
        folder = self.config.get('PathFolder').get('folderStatus')
        return self.nuevacarpeta(folder)



from plugins.xsales.config import Config

from plugins.xsales.util import createfolder

class ConfigStatus(Config):

    spinner = 'monkey'

    @property
    def filestatus(self):
        folder = self.config.get('PathFolder').get('folderStatus')
        path = createfolder(folder)
        return path



from ...config import Config
from ...util import createfolder

class ConfigStatus(Config):

    spinner = 'monkey'

    @property
    def filestatus(self):
        folder = self.config.get('PathFolder').get('folderStatus')
        path = createfolder(folder)
        return path


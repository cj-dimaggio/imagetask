import os

from imagetask.config import ConfigDef
from imagetask.loaders.base import BaseLoader


class FileLoader(BaseLoader):
    config = ConfigDef(dict(
        BASE_PATH=ConfigDef.RequiredField
    ))

    def exists(self, path):
        return os.path.exists(self.full_path(path))

    def get(self, path):
        return open(self.full_path(path), 'rb')

    def full_path(self, path):
        return os.path.join(self.config.BASE_PATH, path)

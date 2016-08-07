import os

from imagetask.config import ConfigDef
from .base import IOBase


class FileIO(IOBase):
    config = ConfigDef(dict(
        BASE_PATH=ConfigDef.RequiredField
    ))

    def exists(self, path):
        return os.path.exists(self.full_path(path))

    def get(self, path, mode='rb'):
        return open(self.full_path(path), mode)

    def full_path(self, path):
        return os.path.join(self.config.BASE_PATH, path)

import os

from imagetask.config import ConfigDef, Configurable


class FileIO(Configurable):
    config = ConfigDef(dict(
        BASE_PATH=ConfigDef.RequiredField,
        MAX_FILENAME_LENGTH=255
    ))

    def exists(self, path):
        return os.path.exists(self.full_path(path))

    def get(self, path, mode='rb'):
        try:
            return open(self.full_path(path), mode)
        except FileNotFoundError:
            return None

    def full_path(self, path):
        return os.path.join(self.config.BASE_PATH, path)

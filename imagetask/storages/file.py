import os

from imagetask.config import ConfigDef
from imagetask.storages.base import BaseStorage


class FileStorage(BaseStorage):
    config = ConfigDef(dict(
        BASE_PATH=ConfigDef.RequiredField
    ))

    def exists(self, path):
        return os.path.exists(self.full_path(path))

    def get(self, path):
        return open(self.full_path(path), 'rb')

    def save(self, path, img):
        save_path = self.full_path(path)
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        img.save(save_path)

    def full_path(self, path):
        return os.path.join(self.config.BASE_PATH, path)

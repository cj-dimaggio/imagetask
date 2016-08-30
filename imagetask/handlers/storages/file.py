import os

from ..helpers.file import FileIO
from .base import BaseStorage


class FileStorage(FileIO, BaseStorage):
    def save(self, path, f):
        save_path = self.full_path(path)
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        with open(save_path, 'wb') as o:
            o.write(f.read())
        return f

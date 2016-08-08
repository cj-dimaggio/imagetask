import os

from ..helpers.file import FileIO
from .base import BaseStorage


class FileStorage(FileIO, BaseStorage):
    def save(self, path, img, save_options):
        save_path = self.full_path(path)
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        img.save(save_path, format=img.format, **save_options)
        return self.get(path)

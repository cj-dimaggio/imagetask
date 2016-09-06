import os
import errno
from ..helpers.file import FileIO
from .base import BaseStorage


class FileStorage(FileIO, BaseStorage):
    def save(self, path, f):
        save_path = self.full_path(path)
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

        with open(save_path, 'wb') as o:
            o.write(f.read())
        return f

    def sanitize_key(self, key):
        # Some filesystems have restrictive max filename.
        # To get around this, we'll try to split the filename into paths
        directory, filename = os.path.dirname(key), os.path.basename(key)
        max_size = self.config.MAX_FILENAME_LENGTH
        new_path = [filename[i:i+max_size] for i in range(0, len(filename), max_size)]
        new_path = os.path.join(*new_path)
        return os.path.join(directory, new_path)


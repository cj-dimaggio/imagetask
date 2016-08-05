import os

from imagetask.config import BaseConfig


class BaseStorage(object):
    CONFIG = {
    }

    def __init__(self, config):
        self.config = BaseConfig(self.CONFIG)
        self.config.update(config)

    def exists(self, image_path):
        raise NotImplementedError

    def get(self, image_path):
        raise NotImplementedError

    def save(self, image_path, key, img):
        raise NotImplementedError

    def save_path(self, image_path, key, img):
        return os.path.join(os.path.basename(image_path), key +
                            '.' + img.format.lower())

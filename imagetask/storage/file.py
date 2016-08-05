import os

from imagetask.storage.base import BaseStorage


class FileStorage(BaseStorage):
    CONFIG = {
        'FIND_PATH': None,
        'SAVE_PATH': '/tmp/'
    }

    def exists(self, image_path):
        return os.path.exists(self.image_path(image_path))

    def get(self, image_path):
        return open(self.image_path(image_path))

    def save(self, image_path, key, img):
        save_path = os.path.join(self.config.SAVE_PATH,
                                 self.save_path(image_path, key, img))
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        img.save(save_path)


    def image_path(self, image_path):
        return os.path.join(self.config.BASE_PATH, image_path)

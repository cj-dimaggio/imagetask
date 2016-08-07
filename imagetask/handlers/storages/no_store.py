from .base import BaseStorage


class NoStoreStorage(BaseStorage):

    def exists(self, path):
        return False

    def get(self, path, mode='rb'):
        return None

    def save(self, path, img, save_options):
        return


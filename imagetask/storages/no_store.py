from imagetask.storages.base import BaseStorage


class NoStoreStorage(BaseStorage):

    def exists(self, path):
        return False

    def get(self, path):
        return None

    def save(self, path, img, save_options):
        return


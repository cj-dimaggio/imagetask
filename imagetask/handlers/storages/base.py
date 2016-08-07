class BaseStorage(object):

    def exists(self, path):
        raise NotImplementedError

    def get(self, path, mode='rb'):
        raise NotImplementedError

    def save(self, path, img, save_options):
        raise NotImplementedError


class NoStorage(BaseStorage):

    def exists(self, path):
        return False

    def get(self, path, mode='rb'):
        return None

    def save(self, path, img, save_options):
        return

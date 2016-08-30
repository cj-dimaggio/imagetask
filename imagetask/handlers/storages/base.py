from imagetask.config import Configurable


class BaseStorage(Configurable):

    def exists(self, path):
        raise NotImplementedError

    def get(self, path, mode='rb'):
        raise NotImplementedError

    def save(self, path, f):
        raise NotImplementedError


class NoStorage(BaseStorage):

    def exists(self, path):
        return False

    def get(self, path, mode='rb'):
        return None

    def save(self, path, f):
        return f

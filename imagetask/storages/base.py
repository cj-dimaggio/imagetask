from imagetask.config import ConfigDef


class BaseStorage(object):
    CONFIG = ConfigDef()

    def exists(self, path):
        raise NotImplementedError

    def get(self, path):
        raise NotImplementedError

    def save(self, path, img):
        raise NotImplementedError

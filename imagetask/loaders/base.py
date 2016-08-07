from imagetask.config import ConfigDef


class BaseLoader(object):
    CONFIG = ConfigDef()

    def exists(self, path):
        raise NotImplementedError

    def get(self, path):
        raise NotImplementedError

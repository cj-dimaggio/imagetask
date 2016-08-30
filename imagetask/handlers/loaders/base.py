from imagetask.config import Configurable


class BaseLoader(Configurable):
    def get(self, path, mode='rb'):
        raise NotImplementedError

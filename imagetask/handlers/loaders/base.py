class BaseLoader(object):
    def get(self, path, mode='rb'):
        raise NotImplementedError

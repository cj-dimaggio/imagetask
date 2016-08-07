class BaseStorage(object):

    def exists(self, path):
        raise NotImplementedError

    def get(self, path, mode='rb'):
        raise NotImplementedError

    def save(self, path, img, save_options):
        raise NotImplementedError

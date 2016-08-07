class BaseLookup(object):

    def exists(self, key):
        raise NotImplementedError

    def add(self, key, value=True):
        raise NotImplementedError


class NoLookup(BaseLookup):

    def exists(self, key):
        return False

    def add(self, key, value=True):
        pass

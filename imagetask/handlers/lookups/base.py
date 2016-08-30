from imagetask.config import Configurable


class BaseLookup(Configurable):

    def exists(self, key):
        raise NotImplementedError

    def add(self, key, value=True):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError


class NoLookup(BaseLookup):

    def exists(self, key):
        return False

    def add(self, key, value=True):
        pass

    def get(self, key):
        return None

    def delete(self, key):
        pass


class WerkzeugWrapper(BaseLookup):

    cache = None

    def exists(self, key):
        return self.cache.has(key)

    def add(self, key, value=True):
        self.cache.set(key, value)

    def get(self, key):
        return self.cache.get(key)

    def delete(self, key):
        self.cache.delete(key)


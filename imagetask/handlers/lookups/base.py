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
        # Has is an optional field
        if hasattr(self.cache, 'has'):
            return self.cache.has(key)
        else:
            return bool(self.cache.get(key))

    def add(self, key, value=True):
        # Default timeout doesn't work for previous versions of werkzeug
        timeout = self.config.get('TIMEOUT', 0)
        self.cache.set(key, value, timeout=timeout)

    def get(self, key):
        return self.cache.get(key)

    def delete(self, key):
        self.cache.delete(key)


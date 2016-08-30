from imagetask.handlers.lookups.base import BaseLookup


class MemoryLookup(BaseLookup):

    def __init__(self, *args, **kwargs):
        self.lookup = dict()
        super(MemoryLookup, self).__init__(*args, **kwargs)

    def exists(self, key):
        return self.lookup.get(key, False)

    def add(self, key, value=True):
        self.lookup[key] = value

    def get(self, key):
        return self.lookup.get(key, None)

    def delete(self, key):
        del self.lookup[key]

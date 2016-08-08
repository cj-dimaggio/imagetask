from imagetask.handlers.lookups.base import BaseLookup


class MemoryLookup(BaseLookup):

    def __init__(self):
        self.lookup = dict()

    def exists(self, key):
        return self.lookup.get(key, False)

    def add(self, key, value=True):
        self.lookup[key] = value

    def delete(self, key):
        del self.lookup[key]

from imagetask.config import ConfigDef


class IOBase(object):

    config = ConfigDef()

    def __init__(self):
        # We want to define the config as a class attribute but we don't want
        # them to get overwritten through multiple inheritance
        self.config = self.config.copy()

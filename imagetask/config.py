class Config(object):

    def __init__(self, config):
        self.update(config)

    def update(self, config):
        for key, value in config.iteritems():
            setattr(self, key, value)

    SECRET_KEY = None
    BASE_URL = None

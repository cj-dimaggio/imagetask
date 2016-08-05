class BaseConfig(object):

    def __init__(self, config):
        self.update(config)

    def update(self, config):
        for key, value in config.iteritems():
            setattr(self, key.upper(), value)


class AppConfig(BaseConfig):

    SECRET_KEY = None
    STORAGE = 'imagetask.storage.file.FileStorage'

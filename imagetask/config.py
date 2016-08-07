from .util import import_class


class ConfigDef(object):
    RequiredField = object()

    def __init__(self, config=None, location=None):
        config = config or dict()
        self.config = config
        self.update(config)
        self.location = location or list()

    def copy(self):
        import copy
        return copy.deepcopy(self)

    def update(self, config):
        self.config.update(config)
        for key, value in config.iteritems():
            key = key.upper()
            setattr(self, key, value)
            self.config[key] = value

    def validate(self):
        for key, value in self.config.iteritems():
            if value == ConfigDef.RequiredField:
                raise Exception(
                    'Required field: "%s" not entered:' % (
                        self.pretty_location() + key))

    def load_class(self, key):
        key = key.upper()
        config = getattr(self, key, None)
        if not config:
            raise Exception('No configuration for key: %s' % key)
        if 'CLASS' not in config:
            raise Exception(
                '%s configuration does not specify a CLASS field' % key)
        return import_class(config.pop('CLASS')), config

    def create_configured_instance(self, key, *args, **kwargs):
        clz, config = self.load_class(key)
        instance = clz(*args, **kwargs)

        if hasattr(instance, 'config') and isinstance(instance.config,
                                                      ConfigDef):
            instance.config.update(config)
            instance.config.location.append(key.upper())
            instance.config.validate()

        return instance

    def pretty_location(self):
        resp = ''
        for loc in self.location:
            resp += '%s: ' % loc
        return resp

    def __getitem__(self, key):
        return self.config[key]

from werkzeug.contrib.cache import RedisCache

from imagetask.config import ConfigDef
from imagetask.handlers.lookups.base import WerkzeugWrapper


class RedisLookup(WerkzeugWrapper):
    config = ConfigDef(dict(
        HOST='localhost',
        PORT=6379,
        PASSWORD=None,
        DB=0,
        KEY_PREFIX='imagetask:',
        TIMEOUT=0
    ))

    def __init__(self, *args, **kwargs):
        super(RedisLookup, self).__init__(*args, **kwargs)
        self.cache = RedisCache(host=self.config['HOST'],
                                port=self.config['PORT'],
                                password=self.config['PASSWORD'],
                                db=self.config['DB'],
                                key_prefix=self.config['KEY_PREFIX'],
                                default_timeout=self.config['TIMEOUT'])

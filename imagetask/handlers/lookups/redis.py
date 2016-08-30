from werkzeug.contrib.cache import RedisCache

from imagetask.config import ConfigDef
from imagetask.handlers.lookups.base import WerkzeugWrapper


class FileLookup(WerkzeugWrapper):
    config = ConfigDef(dict(
        HOST='localhost',
        PORT=6379,
        PASSWORD=None,
        DB=0,
        KEY_PREFIX=None
    ))

    def __init__(self, *args, **kwargs):
        super(FileLookup, self).__init__(*args, **kwargs)
        self.cache = RedisCache(host=self.config['HOST'],
                                port=self.config['PORT'],
                                password=self.config['PASSWORD'],
                                DB=self.config['DB'],
                                key_prefix=self.config['KEY_PREFIX'])

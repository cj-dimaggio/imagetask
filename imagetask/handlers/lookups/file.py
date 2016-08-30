from werkzeug.contrib.cache import FileSystemCache

from imagetask.config import ConfigDef
from imagetask.handlers.lookups.base import WerkzeugWrapper


class FileLookup(WerkzeugWrapper):

    config = ConfigDef(dict(
        CACHE_DIR=ConfigDef.RequiredField,
        THRESHOLD=1000,
        MODE=384
    ))

    def __init__(self, *args, **kwargs):
        super(FileLookup, self).__init__(*args, **kwargs)
        self.cache = FileSystemCache(cache_dir=self.config['CACHE_DIR'],
                                     threshold=self.config['THRESHOLD'],
                                     mode=self.config['MODE'],
                                     default_timeout=0)

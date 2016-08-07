import os
import requests

from imagetask.config import ConfigDef
from .base import BaseLoader


class HTTPLoader(BaseLoader):

    config = ConfigDef({
        'BASE': ''
    })

    def get(self, path, mode='rb'):
        return requests.get(os.path.join(self.config.BASE, path))

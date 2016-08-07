from itsdangerous import URLSafeSerializer

from .image.spec import ImageSpec
from .config import ConfigDef


class ImageTaskApp(object):
    config = ConfigDef(dict(
        SECRET_KEY=ConfigDef.RequiredField,
        LOADER={
            'CLASS': 'imagetask.handlers.loaders.file.FileLoader'
        },
        STORAGE={
            'CLASS': 'imagetask.handlers.storages.base.NoStorage',
            'BASE_PATH': '/tmp/'
        },
        LOOKUP={
            'CLASS': 'imagetask.handlers.lookups.memory.MemoryLookup'
        }
    ))

    def __init__(self, config):
        self.config = self.config.copy()
        self.config.update(config)
        self.config.validate()
        self.serializer = URLSafeSerializer(self.config.SECRET_KEY)

        self.loader = self.config.create_configured_instance('LOADER')
        self.storage = self.config.create_configured_instance('STORAGE')
        self.lookup = self.config.create_configured_instance('LOOKUP')

    def derivative(self, image_path, processors=None, save_options=None):
        return ImageSpec(self, image_path, processors=processors,
                         save_options=save_options)

    def from_serial_data(self, serial_data):
        return ImageSpec.create_from_serial_data(self, serial_data)

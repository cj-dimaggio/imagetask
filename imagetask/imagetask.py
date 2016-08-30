from itsdangerous import URLSafeSerializer

from imagetask.util import import_class
from .image.spec import ImageSpec
from .config import ConfigDef


class ImageTaskApp(object):
    config = ConfigDef(dict(
        SECRET_KEY=ConfigDef.RequiredField,
        URL_PREFIX='',
        IMAGE_SPEC_CLASS='imagetask.image.spec.ImageSpec',
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

        self.spec_class = import_class(self.config['IMAGE_SPEC_CLASS'])

        self.loader = self.config.create_configured_instance('LOADER')
        self.storage = self.config.create_configured_instance('STORAGE')
        self.lookup = self.config.create_configured_instance('LOOKUP')

    def new(self, image_path, processors=None, save_options=None):
        return self.spec_class(self, image_path, processors=processors,
                               save_options=save_options)

    def derivative(self, image_path, processors=None, save_options=None):
        # Backwards compatibility
        return self.new(image_path, processors, save_options)

    def from_serial_data(self, serial_data):
        return self.spec_class.create_from_serial_data(self, serial_data)

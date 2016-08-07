from itsdangerous import URLSafeSerializer

from .handlers.spec import ImageSpec
from .config import ConfigDef


class ImageTaskApp(object):
    config = ConfigDef(dict(
        SECRET_KEY=ConfigDef.RequiredField,
        LOADER={
            'CLASS': 'imagetask.loaders.file.FileLoader'
        },
        STORAGE={
            'CLASS': 'imagetask.storages.no_store.NoStoreStorage',
            'BASE_PATH': '/tmp/'
        }
    ))

    def __init__(self, config):
        self.config.update(config)
        self.config.validate()
        self.serializer = URLSafeSerializer(self.config.SECRET_KEY)

        self.loader = self.config.create_configured_instance('LOADER')
        self.storage = self.config.create_configured_instance('STORAGE')

    def derivative(self, image_path, processors=None, save_options=None):
        return ImageSpec(self, image_path, processors=processors,
                         save_options=save_options)

    def from_serial_data(self, serial_data):
        return ImageSpec.create_from_serial_data(self, serial_data)

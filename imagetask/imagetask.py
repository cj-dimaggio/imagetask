from itsdangerous import URLSafeSerializer

from .handlers.spec import ImageSpec
from .config import ConfigDef


class ImageTaskApp(object):

    config = ConfigDef(dict(
        SECRET_KEY=ConfigDef.RequiredField,
        STORAGE='imagetask.storages.file.FileStorage'
    ))

    def __init__(self, config):
        self.config.update(config)
        self.config.validate()
        self.serializer = URLSafeSerializer(self.config.SECRET_KEY)

        self.storage = self.config.create_configured_instance('STORAGE')

    def derivative(self, image_path, processors=None):
        return ImageSpec(self, image_path, processors=processors)

    def from_serial_data(self, serial_data):
        return ImageSpec.create_from_serial_data(self, serial_data)


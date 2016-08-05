from itsdangerous import URLSafeSerializer

from .util import import_class
from .define.spec import ImageSpec
from .define.processor import ProcessorChain
from .config import AppConfig


class ImageTaskApp(object):

    def __init__(self, config):
        self.config = AppConfig(config)
        self.serializer = URLSafeSerializer(self.config.SECRET_KEY)

        storage_cls = import_class(self.config.STORAGE)
        self.storage = storage_cls(getattr(self.config, self.config.STORAGE.upper()))

    def new_processor_chain(self, image_path, processes=None):
        return ProcessorChain(self, image_path, processes)

    def new_image_spec(self, serial_data):
        return ImageSpec(self, serial_data)


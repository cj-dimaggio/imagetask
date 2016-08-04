from itsdangerous import URLSafeSerializer

from .define.spec import ImageSpec
from .define.processor import ProcessorChain
from .config import Config


class ImageTaskApp(object):

    def __init__(self, config):
        self.config = Config(config)
        self.serializer = URLSafeSerializer(self.config.SECRET_KEY)

    def new_processor_chain(self, image_path, processes=None):
        return ProcessorChain(self, image_path, processes)

    def new_image_spec(self, serial_data):
        return ImageSpec(self, serial_data)

    def get_image(self, image_path):
        import os
        from PIL import Image
        return Image.open(os.path.join(self.config.BASE_PATH, image_path))

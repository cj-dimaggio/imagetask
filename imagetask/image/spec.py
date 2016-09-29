import os
from six import string_types, BytesIO

from PIL import Image

from imagetask.processors import ProcessorMeta
from imagetask.util import import_class
from collections import deque


class ImageSpec(object):
    def __init__(self, app, image_path, processors=None, save_options=None):
        self.app = app
        self.image_path = image_path
        self.save_options = save_options or dict()

        if isinstance(processors, list):
            processors = deque(processors)
        self.processors = processors or deque()

    def serialize(self):
        return self.app.serializer.dumps((
            self.image_path,
            self.flatten_processes(self.processors),
            self.save_options
        ))

    def _perform_img_processors(self):
        img = Image.open(self.app.loader.get(self.image_path))

        # Processors will probably convert image to raw rgb
        img_format = self.determine_save_format(img)

        for proc in self.processors:
            img = proc.process(img)

        img.format = img_format
        return img

    def _generate_image(self):
        img = self._perform_img_processors()

        save_options = self.save_options.copy()
        save_options.pop('format', None)
        save_options.pop('maintain_alpha', None)
        f = BytesIO()
        img.save(f, format=img.format, **save_options)
        f.seek(0)
        self.app.storage.save(self.app.storage.sanitize_key(self.key), f)
        f.seek(0)
        return f

    def generate(self):
        key = self.key
        storage_key = self.app.storage.sanitize_key(key)

        resp = None

        if self.app.lookup.exists(key):
            resp = self.app.storage.get(storage_key)
            if not resp:
                # The cache gave a bad response, so unset the key
                self.app.lookup.delete(key)

        if not resp:
            if self.app.storage.exists(storage_key):
                # We had a cache miss (for some reason) and will want
                # to add it later
                resp = self.app.storage.get(storage_key)
            else:
                resp = self._generate_image()
            self.app.lookup.add(key)

        if resp:
            resp.seek(0)

        return resp

    def determine_save_format(self, img):
        if self.save_options.get('format'):
            if self.save_options.get('maintain_alpha',
                                     False) and img.mode in ['RGBA', 'L']:
                alpha = img.split()[-1]
                all_pixel = alpha.width * alpha.height
                if alpha.histogram()[255] != all_pixel:
                    return img.format
            else:
                return self.save_options.get('format')
        return img.format

    def copy(self):
        # Support this class being extended
        clz = self.__class__
        return clz(self.app, self.image_path, processors=self.processors,
                   save_options=self.save_options)

    def new_processor(self, processor):
        return self.append_processor_copy(processor)

    def append_processor_copy(self, processor):
        copy = self.copy()
        copy.processors.append(processor)
        return copy

    def prepend_processor_copy(self, processor):
        copy = self.copy()
        copy.processors.appendleft(processor)
        return copy

    def crop(self, width=None, height=None, x=None, y=None):
        from imagetask.processors import Crop
        return self.new_processor(
            Crop(width=width, height=height, x=x, y=y))

    def resize(self, width=None, height=None):
        from imagetask.processors import ScaleToFit
        return self.new_processor(ScaleToFit(width, height))

    def resize_to_cover(self, width, height):
        from imagetask.processors import ResizeToCover
        return self.new_processor(ResizeToCover(width, height))

    def max_dimensions(self, width=None, height=None, upscale=False,
                       mat_color=None):
        from imagetask.processors import ResizeToFit
        return self.new_processor(
            ResizeToFit(width, height, upscale, mat_color))

    @property
    def key(self):
        return self.serialize()

    @property
    def url(self):
        return os.path.join(self.app.config.URL_PREFIX, self.key)

    @classmethod
    def create_from_serial_data(cls, app, serial_data):
        data = app.serializer.loads(serial_data)
        image_path = data[0]
        processors = cls.expand_processes(data[1])
        save_options = data[2]
        return cls(app, image_path, processors=processors,
                   save_options=save_options)

    @staticmethod
    def flatten_processes(processes=None):
        processes = processes or list()
        resp = list()
        for proc in processes:
            if isinstance(proc.__class__, ProcessorMeta):
                class_name = '%s.%s' % (
                    proc.__class__.__module__, proc.__class__.__name__)
                resp.append((class_name, proc._spec.get('args'),
                             proc._spec.get('kwargs')))
        return resp

    @staticmethod
    def expand_processes(processes=None):
        processes = processes or list()
        resp = list()
        for proc in processes:
            clz = import_class(proc[0])
            resp.append(clz(*proc[1], **proc[2]))
        return resp

    def __add__(self, other):
        if isinstance(other, string_types):
            return self.url + other
        elif isinstance(other.__class__, ProcessorMeta):
            return self.append_processor_copy(other)

    def __radd__(self, other):
        if isinstance(other, string_types):
            return other + self.url
        elif isinstance(other.__class__, ProcessorMeta):
            return self.prepend_processor_copy(other)

    def __repr__(self):
        return self.url

    def __str__(self):
        return self.url

    def __unicode__(self):
        return self.url

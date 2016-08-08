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

    def generate(self):
        key = self.url

        if not self.app.lookup.exists(key):
            if not self.app.storage.exists(key):
                img = Image.open(self.app.loader.get(self.image_path))

                # Processors will probably convert image to raw rgb
                img_format = self.determine_save_format(img)

                for proc in self.processors:
                    img = proc.process(img)

                img.format = img_format

                save_options = self.save_options.copy()
                save_options.pop('format', None)
                save_options.pop('maintain_alpha', None)
                f = self.app.storage.save(key, img, save_options)
                self.app.lookup.add(key)
                return f
            else:
                # We had a cache miss (for some reason) and want to add it
                self.app.lookup.add(key)
        return self.app.storage.get(key)

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
        return ImageSpec(self.app, self.image_path, processors=self.processors,
                         save_options=self.save_options)

    def append_processor_copy(self, processor):
        copy = self.copy()
        copy.processors.append(processor)
        return copy

    def prepend_processor_copy(self, processor):
        copy = self.copy()
        copy.processors.appendleft(processor)
        return copy

    @property
    def url(self):
        return self.serialize()

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
        if isinstance(other, basestring):
            return self.url + other
        elif isinstance(other.__class__, ProcessorMeta):
            return self.append_processor_copy(other)

    def __radd__(self, other):
        if isinstance(other, basestring):
            return other + self.url
        elif isinstance(other.__class__, ProcessorMeta):
            return self.prepend_processor_copy(other)

    def __repr__(self):
        return self.url

    def __str__(self):
        return self.url

    def __unicode__(self):
        return self.url

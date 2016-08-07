from PIL import Image

from imagetask.processors import ProcessorMeta
from imagetask.util import import_class
from collections import deque


class ImageSpec(object):
    def __init__(self, app, image_path, processors=None, options=None):
        self.app = app
        self.image_path = image_path
        self.options = options

        if isinstance(processors, list):
            processors = deque(processors)
        self.processors = processors or deque()

    def serialize(self):
        return self.app.serializer.dumps((
                self.image_path,
                self.flatten_processes(self.processors),
                self.options
        ))

    def generate(self):
        img = Image.open(self.app.storage.get(self.image_path))
        original_format = img.format

        for proc in self.processors:
            img = proc.process(img)

        img.format = original_format
        self.app.storage.save(self.image_path, self.url, img)
        return img

    def copy(self):
        return ImageSpec(self.app, self.image_path, processors=self.processors,
                         options=self.options)

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
        options = data[2]
        return cls(app, image_path, processors=processors, options=options)

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

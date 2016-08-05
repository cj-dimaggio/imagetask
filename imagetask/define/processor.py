from PIL import Image
from collections import deque
from spec import ImageSpec
from imagetask.processors import ProcessorMeta


class ProcessorChain(object):
    def __init__(self, app, image_path, processes=None):
        if isinstance(processes, list):
            processes = deque(processes)

        self.app = app
        self.image_path = image_path
        self.processes = processes or deque()

    def copy(self):
        return ProcessorChain(self.app, self.image_path, self.processes)

    def append_processor_copy(self, process):
        copy = self.copy()
        copy.processes.append(process)
        return copy

    def prepend_processor_copy(self, process):
        copy = self.copy()
        copy.processes.appendleft(process)
        return copy

    def generate(self):
        img = Image.open(self.app.storage.get(self.image_path))
        original_format = img.format

        for proc in self.processes:
            img = proc.process(img)

        img.format = original_format
        self.app.storage.save(self.image_path, self.url, img)
        return img

    @property
    def url(self):
        return ImageSpec.serialize_spec(self.app.serializer, self.image_path,
                                        self.processes)

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

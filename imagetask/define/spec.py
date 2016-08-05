from imagetask.processors import ProcessorMeta
from imagetask.util import import_class


class ImageSpec(object):
    def __init__(self, app, serial_data):
        self.app = app
        data = self.app.serializer.loads(serial_data)
        self.image_path = data[0]
        self.processor_chain = self.app.new_processor_chain(self.image_path,
                                                      self.expand_processes(
                                                          data[1]))

    def serialize(self):
        return self.serialize_spec(self.image_path, self.processes)

    def generate(self):
        return self.processor_chain.generate()

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

    @staticmethod
    def serialize_spec(serializer, image_path, processes=None):
        processes = ImageSpec.flatten_processes(processes)

        return serializer.dumps((
            image_path,
            processes
        ))

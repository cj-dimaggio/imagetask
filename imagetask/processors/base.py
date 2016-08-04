from functools import wraps


class ProcessorMeta(type):
    def __new__(mcs, name, parents, dct):

        def wrap_init(func):
            @wraps(func)
            def processed_init(self, *args, **kwargs):
                self._spec = dict(args=args, kwargs=kwargs)
                func(self, *args, **kwargs)
            return processed_init

        if '__init__' in dct:
            dct['__init__'] = wrap_init(dct.get('__init__'))

        return super(ProcessorMeta, mcs).__new__(mcs, name, parents, dct)


class CustomProcessorBase(object):
    __metaclass__ = ProcessorMeta

    def process(self, img):
        raise NotImplementedError

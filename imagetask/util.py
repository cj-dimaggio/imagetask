from importlib import import_module


def import_class(clz_path):
    module, clz = clz_path.rsplit('.', 1)
    try:
        module = import_module(module)
        return getattr(module, clz)
    except ImportError as e:
        raise Exception('Unable to import: %s. Exception: %s' % (clz_path, e))

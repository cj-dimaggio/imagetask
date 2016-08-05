from importlib import import_module


def import_class(clz_path):
    module, clz = clz_path.rsplit('.', 1)
    module = import_module(module)
    return getattr(module, clz)

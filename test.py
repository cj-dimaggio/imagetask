from imagetask.imagetask import ImageTaskApp
from imagetask.processors import Transpose

config = {
    'BASE_PATH': '/Users/cjdimaggio/Downloads',
    'SECRET_KEY': 'SECRET',
    'LOADER': {
        'CLASS': 'imagetask.loaders.file.FileLoader',
        'BASE_PATH': '/Users/cjdimaggio/Downloads'
    },
    'STORAGE': {
        'CLASS': 'imagetask.storages.file.FileStorage',
        'BASE_PATH': '/tmp/'
    }
}

imagetask = ImageTaskApp(config)

proc = imagetask.derivative('911-obama-optimized.JPG')
proc += Transpose(Transpose.FLIP_HORIZONTAL)
print proc.url
spec = imagetask.from_serial_data(proc.url)
img = spec.generate()

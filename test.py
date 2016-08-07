from imagetask.imagetask import ImageTaskApp
from imagetask.processors import Transpose

config = {
    'BASE_PATH': '/Users/cjdimaggio/Downloads',
    'SECRET_KEY': 'SECRET',
    'LOADER': {
        'CLASS': '',
        'BASE_PATH': ''
    },
    'STORAGE': {
        'CLASS': 'imagetask.storages.file.FileStorage',
        'BASE_PATH': '/Users/cjdimaggio/Downloads'
    }
}

imagetask = ImageTaskApp(config)

proc = imagetask.derivative('911-obama-optimized.JPG')
proc += Transpose(Transpose.FLIP_HORIZONTAL)
print proc.url
spec = imagetask.from_serial_data(proc.url)
img = spec.generate()

from imagetask.imagetask import ImageTaskApp
from imagetask.processors import Transpose

config = {
    'BASE_PATH': '/Users/cjdimaggio/Downloads',
    'SECRET_KEY': 'SECRET',
    'STORAGE': 'imagetask.storage.file.FileStorage',
    'imagetask.storage.file.FileStorage': {
        'FIND_PATH': '/Users/cjdimaggio/Downloads'
    }
}

imagetask = ImageTaskApp(config)

proc = imagetask.new_processor_chain('911-obama-optimized.JPG')
proc += Transpose(Transpose.FLIP_HORIZONTAL)
print proc.url
spec = imagetask.new_image_spec(proc.url)
img = spec.generate()

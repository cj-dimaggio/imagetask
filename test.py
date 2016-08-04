from imagetask.imagetask import ImageTaskApp
from imagetask.processors import Reflection

config = {
    'BASE_PATH': '/Users/cjdimaggio/Download',
    'SECRET_KEY': 'SECRET'
}

imagetask = ImageTaskApp(config)

proc = imagetask.new_processor_chain('911-obama-optimized.JPG')
proc += Reflection()
print proc.url
spec = imagetask.new_image_spec(proc.url)
pass

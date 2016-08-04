import os
from PIL import Image
import pilkit
from itsdangerous import URLSafeSerializer


def send(secret_key, image_path, procs):
    data = {
        'image_path': image_path,
        'procs': procs
    }

    serializer = URLSafeSerializer(secret_key)
    return serializer.dumps(data)


def read(secret_key, data, base_path):
    def crop(img, x=0, y=0, w=None, h=None):
        return img.crop((x, y, w, h))

    def resize(img, x, y):
        return img.resize((x, y))

    process = {
        'crop': crop,
        'resize': resize
    }

    serializer = URLSafeSerializer(secret_key)
    data = serializer.loads(data)
    path = os.path.join(base_path, data.get('image_path', ''))
    img = Image.open(open(path))
    for proc in data.get('procs', []):
        img = process.get(proc[0], lambda _: img)(img, **proc[1])

if __name__ == '__main__':
    data = send('SECRET', '911-obama-optimized.JPG', [
        ('crop', dict(x=0, y=0, w=600, h=600)),
        ('resize', dict(x=1200, y=200))
    ])
    read('SECRET', data, '/Users/cjdimaggio/Downloads')

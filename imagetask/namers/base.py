import os


class BaseNamer(object):
    format_to_extension = {
        'PNG': 'png',
        'GIF': 'gif',
        'PPM': 'ppm',
        'BMP': 'bmp',
        'JPEG': 'jpg',
        'TIFF': 'tif',
    }

    def __init__(self, app):
        self.app = app

    def name(self, image_path, key, img):
        filename = os.path.basename(image_path)
        return '%s/%s.%s' % (
            filename, key, self.format_to_extension.get(img.format, '.jpg'))

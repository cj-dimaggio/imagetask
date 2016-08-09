from PIL import Image
from flask import send_file

from imagetask import ImageTaskApp


def register_imagetask(app, config, route_prefix='',
                       get_endpoint='imagetask_get'):
    imagetask = ImageTaskApp(config)
    app.imagetask = imagetask

    @app.route('%s/<data>' % route_prefix, methods=('GET',),
               endpoint=get_endpoint)
    def get(data):
        f = imagetask.from_serial_data(data).generate()
        img = Image.open(f)
        f.seek(0)
        return send_file(f, 'image/%s' % img.format.lower())

    return imagetask

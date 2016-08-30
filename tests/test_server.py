import copy
import yaml
from flask import Flask
from PIL import Image

from imagetask import ImageTaskApp
from imagetask.processors import Crop
from imagetask.server.flask_plugin import register_imagetask


def test_server():
    config = yaml.load(open('tests/config/test.yml'))
    flask_app = Flask(__name__)
    register_imagetask(flask_app, copy.deepcopy(config))

    imagetask = ImageTaskApp(config)
    deriv = imagetask.new('test_image.png')
    deriv += Crop(width=700, height=500, x=20, y=30)
    url = deriv.url

    with flask_app.test_client() as c:
        from io import BytesIO
        resp = c.get(url)
        f = BytesIO(resp.data)
        f.seek(0)
        assert resp.content_type == 'image/png'
        img = Image.open(f)
        assert img.format == 'PNG'
        assert img.width == 700
        assert img.height == 500

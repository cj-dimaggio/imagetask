import pytest

from PIL import Image
from imagetask import ImageTaskApp


@pytest.yield_fixture
def basic_app():
    basic_config = {
        'SECRET_KEY': 'SECRET',
        'LOADER': {
            'CLASS': 'imagetask.handlers.loaders.file.FileLoader',
            'BASE_PATH': 'tests/media'
        },
        'STORAGE': {
            'CLASS': 'imagetask.handlers.storages.base.NoStorage',
        }
    }
    yield ImageTaskApp(basic_config)


def test_basic_app(basic_app):
    from imagetask.handlers.loaders.file import FileLoader
    from imagetask.handlers.storages.base import NoStorage

    assert basic_app.config.SECRET_KEY == 'SECRET'
    assert isinstance(basic_app.loader, FileLoader)
    assert isinstance(basic_app.storage, NoStorage)


def test_deriv(basic_app):
    from imagetask.processors.lib import Crop
    deriv = basic_app.derivative('test_image.png')
    deriv += Crop(width=50, height=200, x=20, y=10)
    img = Image.open(deriv.generate())
    assert img.width == 50
    assert img.height == 200


def test_serialization(basic_app):
    from imagetask.processors.lib import Crop
    deriv = basic_app.derivative('test_image.png')
    deriv += Crop(width=50, height=200, x=20, y=10)
    data = deriv.url
    new_deriv = basic_app.from_serial_data(data)
    assert data == new_deriv.url


def test_format(basic_app):
    deriv = basic_app.derivative('test_image.png')
    assert Image.open(deriv.generate()).format == 'PNG'

    deriv = basic_app.derivative('test_image.png', save_options={
        'format': 'JPEG',
        'quality':  20
    })
    assert Image.open(deriv.generate()).format == 'JPEG'


def test_alpha(basic_app):
    deriv = basic_app.derivative('test_alpha.png', save_options={
        'format': 'JPEG',
    })
    assert Image.open(deriv.generate()).format == 'JPEG'

    deriv = basic_app.derivative('test_alpha.png', save_options={
        'format': 'JPEG',
        'maintain_alpha': True
    })
    assert Image.open(deriv.generate()).format == 'PNG'

    deriv = basic_app.derivative('test_image.png', save_options={
        'format': 'JPEG',
        'maintain_alpha': True
    })
    assert Image.open(deriv.generate()).format == 'JPEG'

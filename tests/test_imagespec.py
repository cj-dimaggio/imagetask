import pytest

from PIL import Image
from imagetask import ImageSpec
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


def test_determine_save_format():
    spec = ImageSpec(None, '')
    img = Image.open('tests/media/test_alpha.png')

    spec.save_options = {}
    assert spec.determine_save_format(img).lower() == 'png'

    spec.save_options = {'format': 'jpeg'}
    assert spec.determine_save_format(img).lower() == 'jpeg'

    spec.save_options = {'format': 'jpeg', 'maintain_alpha': True}
    assert spec.determine_save_format(img).lower() == 'png'

    img = Image.open('tests/media/test.jpeg')
    spec.save_options = {}
    assert spec.determine_save_format(img).lower() == 'jpeg'

    img = Image.open('tests/media/test.jpeg')
    spec.save_options = {'format': 'png'}
    assert spec.determine_save_format(img).lower() == 'png'

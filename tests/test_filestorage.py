import shutil
import pytest
import os

from imagetask import ImageTaskApp

@pytest.yield_fixture
def app():
    config = {
        'SECRET_KEY': 'SECRET',
        'LOADER': {
            'CLASS': 'imagetask.handlers.loaders.file.FileLoader',
            'BASE_PATH': 'tests/media'
        },
        'STORAGE': {
            'CLASS': 'imagetask.handlers.storages.file.FileStorage',
            'BASE_PATH': 'tests/working'
        }
    }
    try:
        shutil.rmtree('tests/working/')
    except FileNotFoundError:
        pass
    yield ImageTaskApp(config)
    try:
        shutil.rmtree('tests/working/')
    except FileNotFoundError:
        pass


def test_save(app):
    deriv = app.new('test_image.png')
    deriv.generate()
    assert os.path.exists('tests/working/%s' % app.storage.sanitize_key(deriv.key))


def test_lookup(app):
    triggered = [False]
    result = [False]

    def wrapper(f):
        def wrapped(*args, **kwargs):
            triggered[0] = True
            result[0] = f(*args, **kwargs)
            return result
        return wrapped

    deriv = app.new('test_image.png')
    deriv.generate()

    app.storage.exists = wrapper(app.storage.exists)
    app.lookup.lookup = dict()

    deriv.generate()
    assert triggered[0]
    assert result[0]

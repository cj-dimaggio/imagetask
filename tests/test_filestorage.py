import pytest
import os

from imagetask import ImageTaskApp

@pytest.yield_fixture
def app():
    import glob
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
    yield ImageTaskApp(config)
    files = glob.glob('tests/working/*')
    for f in files:
        os.remove(f)


def test_save(app):
    deriv = app.derivative('test_image.png')
    deriv.generate()
    assert os.path.exists('tests/working/%s' % deriv.url)


def test_lookup(app):
    triggered = [False]
    result = [False]

    def wrapper(f):
        def wrapped(*args, **kwargs):
            triggered[0] = True
            result[0] = f(*args, **kwargs)
            return result
        return wrapped

    deriv = app.derivative('test_image.png')
    deriv.generate()

    app.storage.exists = wrapper(app.storage.exists)

    deriv.generate()
    assert triggered[0]
    assert result[0]

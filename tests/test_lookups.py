import os
import pytest

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
            'CLASS': 'imagetask.handlers.storages.base.NoStorage',
        },
        'LOOKUP': {
            'CLASS': 'imagetask.handlers.lookups.file.FileLookup',
            'CACHE_DIR': 'tests/working'
        }
    }
    files = glob.glob('tests/working/*')
    for f in files:
        os.remove(f)
    yield ImageTaskApp(config)
    files = glob.glob('tests/working/*')
    for f in files:
        os.remove(f)


def test_filelookup(app):
    deriv = app.new('test_image.png')
    deriv.generate()
    assert app.lookup.exists(deriv.key)
    app.lookup.add('test', 'value')
    assert app.lookup.get('test') == 'value'

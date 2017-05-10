import shutil
import pytest


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
            'CLASS': 'imagetask.handlers.storages.base.NoStorage',
        },
        'LOOKUP': {
            'CLASS': 'imagetask.handlers.lookups.file.FileLookup',
            'CACHE_DIR': 'tests/working'
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

def test_filelookup(app):
    deriv = app.new('test_image.png')
    deriv.generate()
    assert app.lookup.exists(deriv.key)
    app.lookup.add('test', 'value')
    assert app.lookup.get('test') == 'value'

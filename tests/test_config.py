from imagetask.config import ConfigDef


def test_required():
    config = ConfigDef({
        'REQUIRED': ConfigDef.RequiredField,
    })
    try:
        config.validate()
    except Exception as e:
        assert str(e) == 'Required field: "REQUIRED" not entered:'


def test_update():
    config = ConfigDef({
        'BASE': ConfigDef.RequiredField,
    })

    value = 'hello, world'
    config.update({'BASE': value})
    assert config.BASE == value


def test_default():
    value = 'default_value'
    config = ConfigDef({
        'BASE': value,
    })

    assert config.BASE == value

from django.utils import translation
from django.utils.translation import gettext_noop

from i18nfield.strings import LazyI18nString


def test_explicit_translation():
    data = {
        'de': 'Hallo',
        'en': 'Hello'
    }
    s = LazyI18nString(data)
    translation.activate('en')
    assert str(s) == 'Hello'
    translation.activate('de')
    assert str(s) == 'Hallo'
    assert bool(s)


def test_create_from_string():
    s = LazyI18nString('{"en": "Hello"}')
    assert s.data == {"en": "Hello"}
    s = LazyI18nString('Invalid JSON')
    assert s.data == 'Invalid JSON'


def test_similar_translations():
    data = {
        'en': 'You',
        'de': 'Sie',
        'de-informal': 'Du'
    }
    s = LazyI18nString(data)
    translation.activate('de')
    assert str(s) == 'Sie'
    translation.activate('de-informal')
    assert str(s) == 'Du'

    data = {
        'en': 'You',
        'de-informal': 'Du'
    }
    s = LazyI18nString(data)
    translation.activate('de')
    assert str(s) == 'Du'
    translation.activate('de-informal')
    assert str(s) == 'Du'

    data = {
        'en': 'You',
        'de': 'Sie'
    }
    s = LazyI18nString(data)
    translation.activate('de')
    assert str(s) == 'Sie'
    translation.activate('de-informal')
    assert str(s) == 'Sie'


def test_missing_default_translation():
    data = {
        'de': 'Hallo',
    }
    s = LazyI18nString(data)
    translation.activate('en')
    assert str(s) == 'Hallo'
    translation.activate('de')
    assert str(s) == 'Hallo'


def test_missing_translation():
    data = {
        'en': 'Hello',
    }
    s = LazyI18nString(data)
    translation.activate('en')
    assert str(s) == 'Hello'
    translation.activate('de')
    assert str(s) == 'Hello'


def test_legacy_string():
    s = LazyI18nString("Hello")
    translation.activate('en')
    assert str(s) == 'Hello'
    translation.activate('de')
    assert str(s) == 'Hello'
    assert bool(s)


def test_none():
    s = LazyI18nString(None)
    assert str(s) == ""
    assert not bool(s)
    s = LazyI18nString("")
    assert str(s) == ""
    assert not bool(s)
    s = LazyI18nString({})
    assert str(s) == ""
    assert not bool(s)


def test_format():
    data = {
        'en': 'You',
        'de': 'Sie'
    }
    s = LazyI18nString(data)
    translation.activate('de')
    assert '{}'.format(s) == 'Sie'


def test_equality():
    data = {
        'en': 'You',
        'de': 'Sie'
    }
    s1 = LazyI18nString(data)
    s2 = LazyI18nString(data.copy())
    s3 = LazyI18nString({'en': 'I', 'de': 'Ich'})
    assert s1 == s2
    assert s2 != s3
    assert s1 != None  # noqa
    assert s1 == data


def test_from_gettext():
    gstr = gettext_noop('Welcome')
    lstr = LazyI18nString.from_gettext(gstr)
    assert 'de' in lstr.data
    assert lstr.data['en'] == 'Welcome'


def test_map():
    data = {
        'de': 'hallo',
        'en': 'hello'
    }
    s = LazyI18nString(data)
    translation.activate('en')
    assert str(s) == 'hello'
    translation.activate('de')
    assert str(s) == 'hallo'
    s.map(lambda s: s.capitalize())
    translation.activate('en')
    assert str(s) == 'Hello'
    translation.activate('de')
    assert str(s) == 'Hallo'

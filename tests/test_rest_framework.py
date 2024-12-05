import json
import pytest
from rest_framework.exceptions import ValidationError

from i18nfield.rest_framework import I18nField, I18nRestFrameworkEncoder
from i18nfield.strings import LazyI18nString


@pytest.mark.parametrize('string', (
    LazyI18nString('foo'),
    LazyI18nString({'en': 'foo', 'de': 'Foo'}),
))
def test_encode_json(string):
    assert json.loads(json.dumps(string, cls=I18nRestFrameworkEncoder)) == string.data


@pytest.mark.parametrize('value,expected', (
    ('something', {'en': 'something'}),
    (None, None),
    (LazyI18nString(None), None),
    (LazyI18nString(1.5), {'en': '1.5'}),
    (LazyI18nString('foo'), {'en': 'foo'}),
    (LazyI18nString({'en': 'foo'}), {'en': 'foo'}),
    (LazyI18nString({'de': 'etwas'}), {'de': 'etwas'}),
    (1.5, {'en': '1.5'}),
))
def test_i18n_field_representation(value, expected):
    assert I18nField().to_representation(value) == expected


@pytest.mark.parametrize('expected,value', (
    ('something', 'something'),
    (None, None),
    (LazyI18nString({'en': 'foo'}), {'en': 'foo'}),
    (LazyI18nString({'de': 'etwas'}), {'de': 'etwas'}),
    (None, {'xz': 'etwas'}),
    (None, {'xz': 2}),
    (None, 1.5),
))
def test_i18n_field_internalisation(value, expected):
    if expected is None:
        with pytest.raises(ValidationError):
            I18nField().to_internal_value(value)
    else:
        assert I18nField().to_internal_value(value) == expected

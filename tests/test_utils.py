import json
import pytest
from decimal import Decimal

from i18nfield.strings import LazyI18nString
from i18nfield.utils import I18nJSONEncoder

from .testapp.models import Book


@pytest.mark.django_db
def test_encode_json():
    data = {
        'de': 'Hallo',
        'en': 'Hello'
    }
    s = LazyI18nString(data)
    jdata = {
        'salutation': s,
        'empty_book': Book(),
        'books': Book.objects.all(),
        'num': Decimal('0.00')
    }
    assert json.loads(json.dumps(jdata, cls=I18nJSONEncoder)) == {
        "salutation": {
            "de": "Hallo", "en": "Hello"
        },
        "empty_book": {"type": "Book", "id": None},
        "books": [],
        'num': '0.00'
    }

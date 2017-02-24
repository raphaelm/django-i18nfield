import pytest

from i18nfield.fields import I18nFieldMixin
from i18nfield.strings import LazyI18nString
from .testapp.models import Author, Book


@pytest.mark.django_db
def test_save_cycle():
    a = Author.objects.create(name='Tolkien')
    title = LazyI18nString({'de': 'Der Herr der Ringe', 'en': 'The Lord of the Rings'})
    abstract = LazyI18nString({'de': 'Frodo will einen Ring zerstören', 'en': 'Frodo tries to destroy a ring'})
    Book.objects.create(author=a, title=title, abstract=abstract)
    b = Book.objects.first()
    b.clean()
    assert b.title == title
    assert b.abstract == abstract


@pytest.mark.django_db
def test_simple_string():
    a = Author.objects.create(name='Tolkien')
    title = 'The Lord of the Rings'
    abstract = 'Frodo tries to destroy a ring'
    Book.objects.create(author=a, title=title, abstract=abstract)
    b = Book.objects.first()
    b.clean()
    assert b.title == title
    assert b.abstract == abstract
    assert isinstance(b.title, LazyI18nString)
    assert isinstance(b.abstract, LazyI18nString)


def test_to_python():
    mx = I18nFieldMixin()
    mx.to_python('A') == LazyI18nString('A')
    mx.to_python(LazyI18nString('A')) == LazyI18nString('A')
    mx.to_python(None) is None

import pytest
from django.core import serializers

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


@pytest.mark.django_db
def test_serialization_json():
    a = Author.objects.create(name='Tolkien')
    title = LazyI18nString({'de': 'Der Herr der Ringe', 'en': 'The Lord of the Rings'})
    abstract = LazyI18nString({'de': 'Frodo will einen Ring zerstören', 'en': 'Frodo tries to destroy a ring'})
    Book.objects.create(author=a, title=title, abstract=abstract)

    # test that book survives being serialized
    old_book = Book.objects.get(pk=1)
    serialized_book = serializers.serialize("json", Book.objects.filter(pk=1))

    for book in serializers.deserialize("json", serialized_book):
        new_book = book.object
        break

    assert old_book == new_book


@pytest.mark.django_db
def test_serialization_xml():
    a = Author.objects.create(name='Tolkien')
    title = LazyI18nString({'de': 'Der Herr der Ringe', 'en': 'The Lord of the Rings'})
    abstract = LazyI18nString({'de': 'Frodo will einen Ring zerstören', 'en': 'Frodo tries to destroy a ring'})
    Book.objects.create(author=a, title=title, abstract=abstract)

    # test that book survives being serialized
    old_book = Book.objects.get(pk=1)
    serialized_book = serializers.serialize("xml", Book.objects.filter(pk=1))
    for book in serializers.deserialize("xml", serialized_book):
        new_book = book.object
        break

    assert old_book == new_book


@pytest.mark.django_db
def test_serialization_yaml():
    a = Author.objects.create(name='Tolkien')
    title = LazyI18nString({'de': 'Der Herr der Ringe', 'en': 'The Lord of the Rings'})
    abstract = LazyI18nString({'de': 'Frodo will einen Ring zerstören', 'en': 'Frodo tries to destroy a ring'})
    Book.objects.create(author=a, title=title, abstract=abstract)

    # test that book survives being serialized
    old_book = Book.objects.get(pk=1)
    serialized_book = serializers.serialize("yaml", Book.objects.filter(pk=1))
    for book in serializers.deserialize("yaml", serialized_book):
        new_book = book.object
        break

    assert old_book == new_book


def test_initializing_with_string_only():
    json = """
[
  {
    "model": "testapp.book",
    "pk": 1,
    "fields": {
      "title": "Der Herr der Ringe",
      "abstract": "Frodo will einen Ring zerstören",
      "author": 1
    }
  }
]
"""

    for book in serializers.deserialize("json", json):
        assert isinstance(book.object.title, LazyI18nString)
        assert book.object.title.data == "Der Herr der Ringe"
        assert isinstance(book.object.abstract, LazyI18nString)
        assert book.object.abstract.data == "Frodo will einen Ring zerstören"

        break

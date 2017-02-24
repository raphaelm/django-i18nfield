import pytest
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory, inlineformset_factory

from i18nfield.forms import I18nFormField, I18nTextInput, I18nModelFormSet, I18nInlineFormSet
from i18nfield.strings import LazyI18nString
from .testapp.models import Author, Book
from .testapp.forms import BookForm, SimpleForm


def test_field_defaults():
    f = I18nFormField(widget=I18nTextInput)
    assert len(f.fields) == 3
    assert f.clean(LazyI18nString('Foo')) == LazyI18nString('Foo')
    assert f.clean(['A', 'B', 'C']) == LazyI18nString({
        'de': 'A', 'en': 'B', 'fr': 'C'
    })


def test_limited_locales():
    f = I18nFormField(widget=I18nTextInput, locales=['de', 'fr'])
    assert len(f.fields) == 2
    assert f.clean(['A', 'B']) == LazyI18nString({
        'de': 'A', 'fr': 'B'
    })
    assert f.widget.enabled_locales == ['de', 'fr']


def test_required():
    f = I18nFormField(widget=I18nTextInput, required=True)
    assert f.clean(['A', ''])
    assert f.clean(['', 'B'])
    with pytest.raises(ValidationError):
        assert f.clean(['', ''])


def test_not_required():
    f = I18nFormField(widget=I18nTextInput, required=False)
    f.clean(['', ''])


def test_max_length():
    f = I18nFormField(widget=I18nTextInput, required=False, max_length=20)
    assert f.clean(['123', ''])
    with pytest.raises(ValidationError):
        f.clean(['1234567890123456789012', ''])


def test_modelform_pass_locales_down():
    bf = BookForm(locales=['de', 'fr'])
    assert bf.fields['title'].widget.enabled_locales == ['de', 'fr']


def test_form_pass_locales_down():
    sf = SimpleForm(locales=['de', 'fr'])
    assert sf.fields['title'].widget.enabled_locales == ['de', 'fr']


@pytest.mark.django_db
def test_modelformset_pass_locales_down():
    a = Author.objects.create(name='Tolkien')
    title = 'The Lord of the Rings'
    abstract = 'Frodo tries to destroy a ring'
    Book.objects.create(author=a, title=title, abstract=abstract)

    FormSetClass = modelformset_factory(Book, form=BookForm, formset=I18nModelFormSet)
    fs = FormSetClass(locales=['de', 'fr'], queryset=Book.objects.all())
    assert fs.forms[0].fields['title'].widget.enabled_locales == ['de', 'fr']
    assert fs.empty_form.fields['title'].widget.enabled_locales == ['de', 'fr']


@pytest.mark.django_db
def test_inlineformset_pass_locales_down():
    a = Author.objects.create(name='Tolkien')
    title = 'The Lord of the Rings'
    abstract = 'Frodo tries to destroy a ring'
    Book.objects.create(author=a, title=title, abstract=abstract)

    FormSetClass = inlineformset_factory(Author, Book, form=BookForm, formset=I18nInlineFormSet)
    fs = FormSetClass(locales=['de', 'fr'], instance=a)
    assert fs.forms[0].fields['title'].widget.enabled_locales == ['de', 'fr']
    assert fs.empty_form.fields['title'].widget.enabled_locales == ['de', 'fr']

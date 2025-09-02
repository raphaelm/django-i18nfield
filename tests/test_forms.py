import pytest
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, modelformset_factory
from django.test import override_settings
from lxml.html import html5parser

from i18nfield.forms import (
    I18nForm, I18nFormField, I18nInlineFormSet, I18nModelFormSet,
    I18nTextInput,
)
from i18nfield.strings import LazyI18nString

from .testapp.forms import BookForm, SimpleForm
from .testapp.models import Author, Book


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


def test_require_all_fields():
    f = I18nFormField(widget=I18nTextInput, require_all_fields=True)
    assert f.clean(['A', 'B', 'C'])
    with pytest.raises(ValidationError):
        f.clean(['A', '', ''])
    with pytest.raises(ValidationError):
        f.clean(['', 'B', ''])
    with pytest.raises(ValidationError):
        f.clean(['', '', 'C'])


def test_require_all_fields_limited_locales():
    f = I18nFormField(widget=I18nTextInput, require_all_fields=True, locales=['de', 'fr'])
    assert f.clean(['A', 'B'])
    with pytest.raises(ValidationError):
        f.clean(['A', ''])
    with pytest.raises(ValidationError):
        f.clean(['', 'B'])


def test_require_all_fields_limited_locales_in_form():
    class SimpleRequiredForm(I18nForm):
        title = I18nFormField(widget=I18nTextInput, require_all_fields=True)

    sf = SimpleRequiredForm({'title_1': 'A'}, locales=['en'])  # de, en, fr
    assert sf.is_valid()
    sf = SimpleRequiredForm({'title_1': 'A', 'title_2': 'B'}, locales=['en', 'fr'])  # de, en, fr
    assert sf.is_valid()
    sf = SimpleRequiredForm({'title_0': 'A', 'title_1': 'B', 'title_2': 'C'}, locales=['de', 'en', 'fr'])
    assert sf.is_valid()
    sf = SimpleRequiredForm({'title_1': 'A', 'title_2': ''}, locales=['en', 'fr'])  # de, en, fr
    assert not sf.is_valid()
    sf = SimpleRequiredForm({'title_1': '', 'title_2': 'B'}, locales=['en', 'fr'])  # de, en, fr
    assert not sf.is_valid()
    sf = SimpleRequiredForm({'title_0': 'A', 'title_1': 'B', 'title_2': ''}, locales=['de', 'en', 'fr'])
    assert not sf.is_valid()


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


def test_widget():
    f = I18nFormField(widget=I18nTextInput, required=False, localize=True)
    rendered = f.widget.render('foo', LazyI18nString({'de': 'Hallo', 'en': 'Hello'}))
    tree = html5parser.fromstring(rendered)
    assert tree[0].attrib == {
        'lang': 'de', 'dir': 'ltr', 'name': 'foo_0', 'type': 'text', 'value': 'Hallo'
    }
    assert tree[1].attrib == {
        'lang': 'en', 'dir': 'ltr', 'name': 'foo_1', 'type': 'text', 'value': 'Hello'
    }
    assert tree[2].attrib == {
        'lang': 'fr', 'dir': 'ltr', 'name': 'foo_2', 'type': 'text'
    }


def test_widget_rtl():
    with override_settings(
        LANGUAGES=[
            ('he', 'Hebrew'),
            ('en', 'English'),
        ]
    ):
        f = I18nFormField(widget=I18nTextInput, required=False, localize=True)
        rendered = f.widget.render('foo', LazyI18nString({'he': 'שלום', 'en': 'Hello'}))

    tree = html5parser.fromstring(rendered)
    assert tree[0].attrib == {
        'lang': 'he', 'dir': 'rtl', 'name': 'foo_0', 'type': 'text', 'value': 'שלום'
    }
    assert tree[1].attrib == {
        'lang': 'en', 'dir': 'ltr', 'name': 'foo_1', 'type': 'text', 'value': 'Hello'
    }


def test_widget_empty():
    f = I18nFormField(widget=I18nTextInput, required=False, localize=True)
    rendered = f.widget.render('foo', [])
    tree = html5parser.fromstring(rendered)
    assert tree[0].attrib == {
        'lang': 'de', 'dir': 'ltr', 'name': 'foo_0', 'type': 'text'
    }
    assert tree[1].attrib == {
        'lang': 'en', 'dir': 'ltr', 'name': 'foo_1', 'type': 'text'
    }
    assert tree[2].attrib == {
        'lang': 'fr', 'dir': 'ltr', 'name': 'foo_2', 'type': 'text'
    }


def test_widget_required():
    f = I18nFormField(widget=I18nTextInput, required=True, localize=True)
    rendered = f.widget.render('foo', LazyI18nString({'de': 'Hallo', 'en': 'Hello'}))
    assert 'required' not in rendered


def test_custom_id():
    f = I18nFormField(widget=I18nTextInput, required=True, localize=True)
    rendered = f.widget.render('foo', LazyI18nString({'de': 'Hallo', 'en': 'Hello'}), attrs={'id': 'bla'})
    assert 'id="bla_0"' in rendered
    assert 'id="bla_1"' in rendered


def test_widget_enabled_locales():
    f = I18nFormField(widget=I18nTextInput, required=False)
    f.widget.enabled_locales = ['de', 'fr']
    rendered = f.widget.render('foo', LazyI18nString({'de': 'Hallo', 'en': 'Hello'}))

    tree = html5parser.fromstring(rendered)
    assert tree[0].attrib == {
        'lang': 'de', 'dir': 'ltr', 'name': 'foo_0', 'type': 'text', 'value': 'Hallo'
    }
    assert tree[1].attrib == {
        'lang': 'fr', 'dir': 'ltr', 'name': 'foo_2', 'type': 'text'
    }


def test_widget_enabled_locales_rtl():
    with override_settings(
        LANGUAGES=[
            ('de', 'German'),
            ('en', 'English'),
            ('he', 'Hebrew'),
        ]
    ):
        f = I18nFormField(widget=I18nTextInput, required=False)
        f.widget.enabled_locales = ['de', 'he']
        rendered = f.widget.render('foo', LazyI18nString({'de': 'Hallo', 'en': 'hello'}))

    tree = html5parser.fromstring(rendered)
    assert tree[0].attrib == {
        'lang': 'de', 'dir': 'ltr', 'name': 'foo_0', 'type': 'text', 'value': 'Hallo'
    }
    assert tree[1].attrib == {
        'lang': 'he', 'dir': 'rtl', 'name': 'foo_2', 'type': 'text'
    }


def test_widget_decompress_naive():
    f = I18nFormField(widget=I18nTextInput, required=False)
    assert f.widget.decompress('Foo') == [
        None, 'Foo', None
    ]


def test_widget_decompress_missing():
    f = I18nFormField(widget=I18nTextInput, required=False)
    assert f.widget.decompress({'de': 'Hallo', 'en': 'Hello'}) == [
        'Hallo', 'Hello', None
    ]


def test_widget_decompress_all_enabled_missing():
    f = I18nFormField(widget=I18nTextInput, required=False)
    f.widget.enabled_locales = ['de', 'fr']
    assert f.widget.decompress({'en': 'Hello'}) == [
        None, 'Hello', 'Hello'
    ]


def test_widget_decompress_first_two_enabled_not_filled():
    f = I18nFormField(widget=I18nTextInput, required=False)
    f.widget.enabled_locales = ['de', 'en', 'fr']
    assert f.widget.decompress({'fr': 'Bonjour'}) == [
        None, None, 'Bonjour'
    ]

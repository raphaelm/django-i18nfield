from i18nfield.admin import I18nModelAdmin
from i18nfield.fields import I18nCharField, I18nTextField

from .testapp.models import Author


def test_model_admin():
    class AuthorAdmin(I18nModelAdmin):
        pass

    admin = AuthorAdmin(Author, None)

    assert I18nCharField in admin.formfield_overrides
    assert I18nTextField in admin.formfield_overrides


def test_model_admin_override():
    class AuthorAdmin(I18nModelAdmin):
        formfield_overrides = {
            I18nCharField: {"test": "marker"},
        }

    admin = AuthorAdmin(Author, None)

    assert admin.formfield_overrides[I18nCharField] == {"test": "marker"}
    assert I18nTextField in admin.formfield_overrides

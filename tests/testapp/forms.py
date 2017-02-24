from i18nfield import forms

from .models import Book


class BookForm(forms.I18nModelForm):
    class Meta:
        model = Book
        fields = ['title', 'abstract', 'author']


class SimpleForm(forms.I18nForm):
    title = forms.I18nFormField(widget=forms.I18nTextInput)

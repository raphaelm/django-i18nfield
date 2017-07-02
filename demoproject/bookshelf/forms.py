from django import forms

from i18nfield import forms as i18nforms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'abstract', 'author']
        widgets = {
            'title': i18nforms.I18nTextInput,
            'abstract': i18nforms.I18nTextarea
        }

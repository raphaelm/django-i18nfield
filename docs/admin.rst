Admin integration
=================

Currently, our fields do not yet automatically integrate with Django admin. By default,
Django admin tries to use a custom widget for the fields which do not work in our case.

There is a workaround by using a custom form to explicitly define the widget classes.

.. code-block:: python

    class BookForm(forms.ModelForm):
        class Meta:
            model = Book
            fields = ['title', 'abstract', 'author']
            widgets = {
                'title': i18nforms.I18nTextInput,
                'abstract': i18nforms.I18nTextarea
            }

    class BookAdmin(admin.ModelAdmin):
        form = BookForm

    admin.site.register(Book, BookAdmin)


.. note::

    It is possible that this can be vastly improved without too much effort.
    We don't use the admin in the projects where we use this library, so we did not research
    this further. We'd be happy to see any contributions here!

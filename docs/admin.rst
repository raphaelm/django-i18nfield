Admin integration
=================

Currently, our fields do not yet automatically integrate with Django admin. By default,
Django admin tries to use a custom widget for the fields which do not work in our case.

There is a workaround by using a custom admin class, which explicitly defines the
widget classes in the background.

.. code-block:: python

    from i18nfield.admin import I18nModelAdmin

    class BookAdmin(I18nModelAdmin):
        pass

    admin.site.register(Book, BookAdmin)

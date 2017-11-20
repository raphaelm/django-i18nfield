Django Restframework integration
================================

We provide a custom ``ModelSerializer`` subclass that is able to serialize and
deserialize internationalized string fields. Since this is the only change
compared to a regular ``ModelSerializer``, you should be able to use
``i18nfield.rest_framework.I18nAwareModelSerializer`` without problems.

.. code-block:: python

    from i18nfield.rest_framework import I18nAwareModelSerializer

    class BookSerializer(I18nAwareModelSerializer):

        class Meta:
            model = Book
            fields = ('title',)

You can also configure a subclass of the default JSON renderer that handles
I18nStrings gracefully, by adding it in your ``settings.py``.

.. code-block:: python
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': ('i18nfield.rest_framework.I18nJSONRenderer',),
    }

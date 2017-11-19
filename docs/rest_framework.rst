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

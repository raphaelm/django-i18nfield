Getting started
===============

First of all, you need to install django-i18nfield::

    $ pip3 install django-i18nfield

You should also check that your ``settings.py`` lists the languages that you want to use:

.. code-block:: python

    from django.utils.translation import ugettext_lazy as _

    LANGUAGES = [
        ('de', _('German')),
        ('en', _('English')),
        ('fr', _('French')),
    ]

Now, let's assume you have a simple django model like the following:

.. code-block:: python

    from django.db import models

    class Book(models.Model):
        title = models.CharField(verbose_name='Book title', max_length=190)
        abstract = models.TextField(verbose_name='Abstract')
        author = models.ForeignKey(Author, verbose_name='Author')

You can change your model to store internationalized data like the following:

.. code-block:: python

    from django.db import models
    from i18nfield.fields import I18nCharField, I18nTextField

    class Book(models.Model):
        title = I18nCharField(verbose_name='Book title', max_length=190)
        abstract = I18nTextField(verbose_name='Abstract')
        author = models.ForeignKey(Author, verbose_name='Author')

And you're done! Really, that's it.

If you now create a ``ModelForm`` for that model, the title and author fields will
consist of multiple language fields, one for each language. They don't look nice yet
and Django admin does not know how to deal with them so far. Also, they no longer
contain standard python strings but ``LazyI18nStrings`` which have some special property.
But luckily for you, we wrote more pages in this documentation, go ahead and check them out. :)

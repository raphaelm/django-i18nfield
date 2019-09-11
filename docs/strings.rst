Working with translated strings
===============================

If you want to save multi-lingual data into an ``I18nCharField`` or ``I18nTextField``,
you need to wrap it as an ``LazyI18nString`` first. Also, if you read data from such
a field, you will always get an ``LazyI18nString`` back.

An ``LazyI18nString`` is a representation of a string that exists in multiple languages.
Under the hood, it is just a dictionary that maps languages to values.

So why don't we just use dictionaries? This is where the "**lazy**" comes into play: As soon
as you try to evaluate an ``LazyI18nString`` as a normal string, it will magically transform
into a normal string -- based on the currently active language. This means that e.g. if you get
a value from an ``I18nCharField`` and pass it to a template, the template will cast the value
to a string and you **do not need to do anything** to make it work.

This behaviour is intentionally very similar to the ``ugettext_lazy`` method from Django's translation
layer.

However, when you deal with such strings in python code, you should know how they behave. Therefore,
we have a number of examples for you on this page.

.. testsetup:: *

   from i18nfield.strings import LazyI18nString

To create a LazyI18nString, we can input a simple string:

.. doctest::

   >>> naive = LazyI18nString('Naive untranslated string')
   >>> naive
   <LazyI18nString: 'Naive untranslated string'>

Or we can provide a dictionary with multiple translations:

.. doctest::

   >>> translated = LazyI18nString(
   ...     {'en': 'English String', 'de': 'Deutscher String'}
   ... )

We can use the ``localize`` method to get the string in a specific language:

.. doctest::

   >>> translated.localize('de')
   'Deutscher String'

   >>> translated.localize('en')
   'English String'

If we try a locale that does not exist for the string, we might get a it either in a similar locale or in the system's default language:

.. doctest::

   >>> translated.localize('de-AT')
   'Deutscher String'

   >>> translated.localize('zh')
   'English String'

   >>> naive.localize('de')
   'Naive untranslated string'

.. important::

   This is an important property of LazyI18nString: **As long as there is any non-empty value for any language, you
   will rather get a result in the wrong language than an empty result.** This makes it "safe" to use if your data is
   only partially translated.

If we cast a ``LazyI18nString`` to ``str``, ``localize`` will be called with the currently active language:

.. doctest::

   >>> from django.utils import translation
   >>> str(translated)
   'English String'
   >>> translation.activate('de')
   >>> str(translated)
   'Deutscher String'

Formatting also works as expected:

.. doctest::

   >>> translation.activate('de')
   >>> '{}'.format(translated)
   'Deutscher String'

If we want to modify all translations inside a ``LazyI18nString`` we can do so using the ``map`` method:

.. doctest::

   >>> translated.map(lambda s: s.replace('String','Text'))
   >>> translation.activate('de')
   >>> str(translated)
   'Deutscher Text'

There is also a way to construct a hybrid object that takes its data from ``gettext`` but behaves like an
``LazyI18nString``. The use case for this is very rare, it basically only is useful when defining default
values for internationalized form fields in the codebase.

.. doctest::

   >>> from django.utils.translation import ugettext_noop
   >>> LazyI18nString.from_gettext(ugettext_noop('Hello'))
   <LazyI18nString: <LazyGettextProxy: 'Hello'>>

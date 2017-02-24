Working with forms
==================

Fields and Widgets
------------------

If you use a ``ModelForm``, you will automatically get an ``I18nFormField`` field
for your internationalized fields with the default widget being either an ``I18nTextInput``
or an ``I18nTextarea`` being the default widget. But of course you can also use these
fields manually as you would use any other field, even completely without touching models.

.. autoclass:: i18nfield.forms.I18nFormField

.. autoclass:: i18nfield.forms.I18nTextInput

.. autoclass:: i18nfield.forms.I18nTextarea


Advanced usage: Restrict the visible languages
----------------------------------------------

Sometimes, you do not want to display fields for all languages every time. If you build a
shopping platform, your platform might support tens or hundreds of languages, while a single
shop only supports a few of them. In this case, the shop owner should not see input fields
for languages that they don't want to support.

As you can see above, ``I18nFormField`` has a constructor argument ``locales`` that takes a
list of locales for this exact purpose. However, most of the time, your ``I18nFormField``
is defined in a way that does not allow you to pass a dynamic list there. Therefore, we provide
a form base class that you can use for your ``ModelForm`` that *also* takes a ``locales`` constructor
argument and passes it through to all its fields.

For the same reason, we provide formset base classes that add the ``locales`` argument to your
formset class and pass it through to all fields.

.. autoclass:: i18nfield.forms.I18nModelForm

.. autoclass:: i18nfield.forms.I18nModelFormSet

.. autoclass:: i18nfield.forms.I18nInlineFormSet


.. note:: As ``I18nFormField`` tries to pass this information down to the widget, this might
          fail if you use a custom widget class that does not inherit from our default widgets.

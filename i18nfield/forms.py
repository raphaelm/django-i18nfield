from typing import List

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from .strings import LazyI18nString


class I18nWidget(forms.MultiWidget):
    """
    The default form widget for I18nCharField and I18nTextField. It makes
    use of Django's MultiWidget mechanism and does some magic to save you
    time.
    """
    widget = forms.TextInput

    def __init__(self, langcodes: List[str], field: forms.Field, attrs=None):
        widgets = []
        self.langcodes = langcodes
        self.enabled_langcodes = langcodes
        self.field = field
        for lng in self.langcodes:
            a = copy.copy(attrs) or {}
            a['lang'] = lng
            widgets.append(self.widget(attrs=a))
        super().__init__(widgets, attrs)

    def decompress(self, value):
        data = []
        first_enabled = None
        any_filled = False
        any_enabled_filled = False
        if not isinstance(value, LazyI18nString):
            value = LazyI18nString(value)
        for i, lng in enumerate(self.langcodes):
            dataline = (
                value.data[lng]
                if value is not None and (
                    isinstance(value.data, dict) or isinstance(value.data, LazyI18nString.LazyGettextProxy)
                ) and lng in value.data
                else None
            )
            any_filled = any_filled or (lng in self.enabled_langcodes and dataline)
            if not first_enabled and lng in self.enabled_langcodes:
                first_enabled = i
                if dataline:
                    any_enabled_filled = True
            data.append(dataline)
        if value and not isinstance(value.data, dict):
            data[first_enabled] = value.data
        elif value and not any_enabled_filled:
            data[first_enabled] = value.localize(self.enabled_langcodes[0])
        return data

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            if self.langcodes[i] not in self.enabled_langcodes:
                continue
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(
                    final_attrs,
                    id='%s_%s' % (id_, i),
                    title=self.langcodes[i]
                )
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
        return mark_safe(self.format_output(output))

    def format_output(self, rendered_widgets):
        return '<div class="i18n-form-group">%s</div>' % super().format_output(rendered_widgets)


class I18nTextInput(I18nWidget):
    widget = forms.TextInput


class I18nTextarea(I18nWidget):
    widget = forms.Textarea


class I18nFormField(forms.MultiValueField):
    """
    The form field that is used by I18nCharField and I18nTextField. It makes use
    of Django's MultiValueField mechanism to create one sub-field per available
    language.

    It contains special treatment to make sure that a field marked as "required" is validated
    as "filled out correctly" if *at least one* translation is filled it. It is never required
    to fill in all of them. This has the drawback that the HTML property ``required`` is set on
    none of the fields as this would lead to irritating behaviour.

    :param langcodes: An iterable of locale codes that the widget should render a field for. If
        omitted, fields will be rendered for all languages supported by pretix.
    """

    def compress(self, data_list):
        langcodes = self.langcodes
        data = {}
        for i, value in enumerate(data_list):
            data[langcodes[i]] = value
        return LazyI18nString(data)

    def clean(self, value):
        if isinstance(value, LazyI18nString):
            # This happens e.g. if the field is disabled
            return value
        found = False
        clean_data = []
        errors = []
        for i, field in enumerate(self.fields):
            try:
                field_value = value[i]
            except IndexError:
                field_value = None
            if field_value not in self.empty_values:
                found = True
            try:
                clean_data.append(field.clean(field_value))
            except forms.ValidationError as e:
                # Collect all validation errors in a single list, which we'll
                # raise at the end of clean(), rather than raising a single
                # exception for the first error we encounter. Skip duplicates.
                errors.extend(m for m in e.error_list if m not in errors)
        if errors:
            raise forms.ValidationError(errors)
        if self.one_required and not found:
            raise forms.ValidationError(self.error_messages['required'], code='required')

        out = self.compress(clean_data)
        self.validate(out)
        self.run_validators(out)
        return out

    def __init__(self, *args, **kwargs):
        fields = []
        defaults = {
            'widget': self.widget,
            'max_length': kwargs.pop('max_length', None),
        }
        self.langcodes = kwargs.pop('langcodes', [l[0] for l in settings.LANGUAGES])
        self.one_required = kwargs.get('required', True)
        kwargs['required'] = False
        kwargs['widget'] = kwargs['widget'](
            langcodes=self.langcodes, field=self, **kwargs.pop('widget_kwargs', {})
        )
        defaults.update(**kwargs)
        for lngcode in self.langcodes:
            defaults['label'] = '%s (%s)' % (defaults.get('label'), lngcode)
            fields.append(forms.CharField(**defaults))
        super().__init__(
            fields=fields, require_all_fields=False, *args, **kwargs
        )

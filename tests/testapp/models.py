from django.db import models
from django.utils.translation import gettext_lazy as _

from i18nfield.fields import I18nCharField, I18nTextField


class Author(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=190)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = I18nCharField(verbose_name='Book title', max_length=190)
    abstract = I18nTextField(verbose_name='Abstract')
    author = models.ForeignKey('Author', verbose_name='Author', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

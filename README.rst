I18nFields for Django
=====================

.. image:: https://img.shields.io/pypi/v/django-i18nfield.svg
   :target: https://pypi.python.org/pypi/django-i18nfield

.. image:: https://readthedocs.org/projects/django-i18nfield/badge/?version=latest
   :target: https://django-i18nfield.readthedocs.io/

.. image:: https://travis-ci.org/raphaelm/django-i18nfield.svg?branch=master
   :target: https://travis-ci.org/raphaelm/django-i18nfield

.. image:: https://codecov.io/gh/raphaelm/django-i18nfield/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/raphaelm/django-i18nfield


This is yet another way to store multi-lingual content in Django_. In contrast to other options
like `django-havd`_, `django-modeltranslation`_ or `django-parler`_ it does not require additonal
database tables and you can reconfigure the available languages without any changes to the database
schema. In constrast to `nece`_, it is not specific to PostgreSQL.

How does it work then? It stores JSON data into a ``TextField``. Yes, this is kinda dirty and violates
the `1NF`_. This makes it harder for non-django based programs to interact directly with your database
and is not perfectly efficient in terms of storage space.
It also lacks the ability to do useful lookups, searches and indices on internationalized fields.
If one of those things are important to you, **this project is not for you**, please choose one of the
ones that we linked above.

However if those limitations are fine for you, this provides you with a very lightweight, easy to use and
flexible solution. This approach has been in use in `pretix`_ for quite a while, so it has been tested in
production. The package contains not only the model fields, but also form fields and everything you need
to get them running.

Features
--------

* Very easy installation
* Internationalized versions of ``CharField`` and ``TextField`` types
* Integrated form fields types and widgets
* Automatic migration from non-localized fields with a simple migration
* Full support for forms and formsets
* Possibility to dynamically limit the displayed languages
* Very basic integration with django admin
* Comprehensive test suite and production-tested

Tested with:

* Python 3.4 to 3.6
* Django 1.9 to 1.11

License
-------
The code in this repository is published under the terms of the Apache License. 
See the LICENSE file for the complete license text.

This project is maintained by Raphael Michel <mail@raphaelmichel.de>. See the
AUTHORS file for a list of all the awesome folks who contributed to this project.

.. _pretix: https://github.com/pretix/pretix
.. _django: https://www.djangoproject.com/
.. _django-havd: https://github.com/KristianOellegaard/django-hvad
.. _django-modeltranslation: https://github.com/deschler/django-modeltranslation
.. _django-parler: https://github.com/django-parler/django-parler
.. _nece: https://pypi.python.org/pypi/nece
.. _1NF: https://en.wikipedia.org/wiki/First_normal_form

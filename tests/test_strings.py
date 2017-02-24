from unittest import TestCase

from django.utils import translation

from i18nfield.strings import LazyI18nString


class I18nStringTest(TestCase):
    """
    This test case tests the LazyI18nString class
    """

    def test_explicit_translation(self):
        data = {
            'de': 'Hallo',
            'en': 'Hello'
        }
        s = LazyI18nString(data)
        translation.activate('en')
        self.assertEqual(str(s), 'Hello')
        translation.activate('de')
        self.assertEqual(str(s), 'Hallo')

    def test_similar_translations(self):
        data = {
            'en': 'You',
            'de': 'Sie',
            'de-informal': 'Du'
        }
        s = LazyI18nString(data)
        translation.activate('de')
        self.assertEqual(str(s), 'Sie')
        translation.activate('de-informal')
        self.assertEqual(str(s), 'Du')

        data = {
            'en': 'You',
            'de-informal': 'Du'
        }
        s = LazyI18nString(data)
        translation.activate('de')
        self.assertEqual(str(s), 'Du')
        translation.activate('de-informal')
        self.assertEqual(str(s), 'Du')

        data = {
            'en': 'You',
            'de': 'Sie'
        }
        s = LazyI18nString(data)
        translation.activate('de')
        self.assertEqual(str(s), 'Sie')
        translation.activate('de-informal')
        self.assertEqual(str(s), 'Sie')

    def test_missing_default_translation(self):
        data = {
            'de': 'Hallo',
        }
        s = LazyI18nString(data)
        translation.activate('en')
        self.assertEqual(str(s), 'Hallo')
        translation.activate('de')
        self.assertEqual(str(s), 'Hallo')

    def test_missing_translation(self):
        data = {
            'en': 'Hello',
        }
        s = LazyI18nString(data)
        translation.activate('en')
        self.assertEqual(str(s), 'Hello')
        translation.activate('de')
        self.assertEqual(str(s), 'Hello')

    def test_legacy_string(self):
        s = LazyI18nString("Hello")
        translation.activate('en')
        self.assertEqual(str(s), 'Hello')
        translation.activate('de')
        self.assertEqual(str(s), 'Hello')

    def test_none(self):
        s = LazyI18nString(None)
        self.assertEqual(str(s), "")
        s = LazyI18nString("")
        self.assertEqual(str(s), "")

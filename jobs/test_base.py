import os
from unittest import skipUnless
from django.test import TestCase, tag
@tag('unit')
class UnitTestCase(TestCase):
  pass


INTEGRATION_TESTING = os.environ.get('INTEGRATION_TESTING', 'True')

@tag('integration')
@skipUnless(INTEGRATION_TESTING, 'skip')
class IntegrationTestCase(TestCase):
  pass

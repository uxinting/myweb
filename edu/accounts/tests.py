"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

'''from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
    def test_ImageFonttruetype(self):
        from PIL import ImageFont
        #ImageFont.truetype('msyh.ttc')'''

from PIL import ImageFont
print ImageFont.truetype('msyh.ttc')

from django.test import TestCase

from app.calc import add 

class CalcTest(TestCase):
    
    def test_add_numbers(self):
        """ test for adding function """
        self.assertEqual(add(1,2), 3)
import unittest
from auth import check_password

class TestRequest(unittest.TestCase):
    def test_lower(self):
        check = check_password('abc')
        self.assertEqual(check, False)

    def test_upper(self):
        check = check_password('ABC')
        self.assertEqual(check, False)

    def test_numbers(self):
        check = check_password('123')
        self.assertEqual(check, False)

    def test_special(self):
        check = check_password('@&%*(*@#')
        self.assertEqual(check, False)

    def test_combination(self):
        self.assertEqual(check_password('abcABC123'), False)
        self.assertEqual(check_password('aA1#'), False)
        self.assertEqual(check_password('abcABC123$%*'), True)
        self.assertEqual(check_password('acA13$'), False)




from crablib.querygen.reader import read
import unittest


class TestHTMLGen(unittest.TestCase):
    def test_body(self):
        query = '/images?images=cat+kitten+dog&name=Mitch'
        expected = {'images': ['cat', 'kitten', 'dog'],
                    'name': 'Mitch'}

        self.assertEqual(read(query), expected)


if __name__ == '__main__':
    unittest.main()

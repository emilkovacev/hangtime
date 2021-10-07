from crablib.querygen.reader import read_query
import unittest


class TestHTMLGen(unittest.TestCase):
    def test_body(self):
        query = '/images?images=cat+kitten+dog&name=Mitch'
        expected = {'images': ['cat', 'kitten', 'dog'],
                    'name': 'Mitch'}

        self.assertEqual(read_query(query), expected)

    def test_many(self):
        query = '/images?images=cat+kitten+dog+cat+hare+mouse+Dog&name=Mitch+Emil'
        expected = {'images': ['cat', 'kitten', 'dog', 'cat', 'hare', 'mouse', 'Dog'],
                    'name': ['Mitch', 'Emil']}

        self.assertEqual(read_query(query), expected)


if __name__ == '__main__':
    unittest.main()

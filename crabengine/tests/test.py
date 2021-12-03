import unittest

from ..generate import generate_html


class TestFormParse(unittest.TestCase):

    def test_generateA(self):
        with open('index.html', 'r') as file:
            html = file.read()
            output = generate_html(html, {'a': True, 'b': False, 'c': False})
            self.assertEqual('A', output.strip('\n'))

    def test_generateB(self):
        with open('index.html', 'r') as file:
            html = file.read()
            output = generate_html(html, {'a': False, 'b': False, 'c': True})
            self.assertEqual('B', output.strip('\n'))

    def test_generateC(self):
        with open('index.html', 'r') as file:
            html = file.read()
            output = generate_html(html, {'a': False, 'b': True, 'c': True})
            self.assertEqual('C', output.strip('\n'))

    def test_generateD(self):
        with open('index.html', 'r') as file:
            html = file.read()
            output = generate_html(html, {'a': False, 'b': True, 'c': False})
            self.assertEqual('D', output.strip('\n'))


if __name__ == '__main__':
    unittest.main()

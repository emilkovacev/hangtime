import unittest

from ..generate import generate_html


class TestFormParse(unittest.TestCase):

    def test_generateA(self):
        with open('crabengine/tests/for.html', 'r') as file:
            html = file.read()
            output = generate_html(html, {'args': ['a', 'b', 'c']})
            expected = '<p>a</p><p>b</p><p>c</p>'
            self.assertEqual(expected, output.replace('\n', '').replace(' ', ''))

    def test_generateB(self):
        with open('crabengine/tests/for.html', 'r') as file:
            html = file.read()
            output = generate_html(html, {'args': 'a'})
            self.assertEqual(output.strip("\n").strip(' '), '<p>a</p>')


if __name__ == '__main__':
    unittest.main()

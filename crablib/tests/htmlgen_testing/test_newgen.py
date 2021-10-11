import unittest
from crablib.htmlgen.newgen import generate_html
from crablib.querygen.reader import read_query, Query


test = """<!DOCTYPE html>
<html>
    <body>
        <h1>Hello {{ name }}!</h1>
        {% for src in images %}
            <img src="{{ src }}" />
        {% endfor %}
    </body>
</html>"""


class TestHTMLGen(unittest.TestCase):
    def test_body(self):
        args: Query = read_query('/images?images=kitten+hamster+pig+goose&name=Emil').images()
        # find absolute path of image name in /images
        output = generate_html(test, args)
        expected = '<!DOCTYPE html><html><body><h1>Hello Emil!</h1></body></html>'
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()

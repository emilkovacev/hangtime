import unittest
from crablib.htmlgen.generate import generate_html


class TestHTMLGen(unittest.TestCase):
    def test_body(self):
        args = {
            'names': ['patrick', 'anthony', 'adam', 'rosina'],
            'hi': 'Hello!',
            'heading': 12,
            'subtitle': True
        }
        html = generate_html('templates/template_multicall.html', args)
        test = f"""<!DOCTYPE html>
<html>
    <body>
        <h1>{args["heading"]}</h1>
        <img src="google.jpg"/>
    </body>
</html>"""
        self.assertEqual(html, test)


if __name__ == '__main__':
    unittest.main()

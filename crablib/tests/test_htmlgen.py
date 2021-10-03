import unittest
from crablib.htmlgen.generate import generate_html


class TestHTMLGen(unittest.TestCase):
    def test_body(self):
        args = {'heading': 12, 'image_filename': 'google.jpg'}
        html = generate_html('templates/template.html', args)
        test = f"""<!DOCTYPE html>
<html>
    <body>
        <h1>{args["heading"]}</h1>
        <img src="google.jpg"/>
    </body>
</html>"""
        self.assertEqual(html, test)

    def test_comment(self):
        args = {'heading': True, 'subtitle': 12, 'image_filename': 'google.jpg'}
        html = generate_html('templates/template.html', args)
        test = f"""<!DOCTYPE html>
<html>
    <body>
        <h1>{args["heading"]}</h1>
        <img src="google.jpg"/>
    </body>
</html>"""
        self.assertEqual(html, test)

    def test_multiline(self):
        args = {'heading': True, 'subtitle': 12*3, 'unused': 'Hey there!'}
        html = generate_html('templates/template_multicall.html', args)
        test = f"""<!DOCTYPE html>
<html>
    <body>
        <h1>{args["heading"]} {args['subtitle']}</h1>
    </body>
</html>"""
        self.assertEqual(html, test)


if __name__ == '__main__':
    unittest.main()

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
        html = generate_html('../templates/template_multicall.html', args)
        test = f"""<!DOCTYPE html>
<html>
    <body>
        <h1>12 True</h1>
                    <i>repeat me!</i>
            patrick
            <p>repeat me!</p>
                    <i>repeat me!</i>
            anthony
            <p>repeat me!</p>
                    <i>repeat me!</i>
            adam
            <p>repeat me!</p>
                    <i>repeat me!</i>
            rosina
            <p>repeat me!</p>
        
        <img src="Hello!"/>
    </body>
</html>
"""
        self.assertEqual(html, test)


if __name__ == '__main__':
    unittest.main()

import unittest
from crablib.htmlgen.genfor import generate_loops


class TestHTMLGen(unittest.TestCase):
    def test_body(self):
        html = generate_loops('templates/for_loops.html', arguments={'names': ['patrick', 'anthony', 'adam', 'rosina'],
                                                                     'hi': 'Hello!'})
        expected = """<!DOCTYPE html>
<html>
    <body>
        anthony
        <p>repeat me!</p>
        adam
        <p>repeat me!</p>
        rosina
        <p>repeat me!</p>
    </body>
</html>"""
        self.assertEqual(expected, html)


if __name__ == '__main__':
    unittest.main()

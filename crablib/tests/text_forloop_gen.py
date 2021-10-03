import unittest
from crablib.htmlgen.genfor import generate_loops


class TestHTMLGen(unittest.TestCase):
    def test_body(self):
        generate_loops('templates/for_loops.html', arguments={})


if __name__ == '__main__':
    unittest.main()

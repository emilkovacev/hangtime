import unittest
from crablib.html import render_obj1


class TestRequest(unittest.TestCase):

    def test_no_body(self):
        input = '<!DOCTYPE html>\n' \
                '<html>\n' \
                '   <body>\n' \
                '       <div>\n' \
                '           Hi {{ name }}!\n' \
                '           {{ images }}\n' \
                '       </div>\n' \
                '   </body>\n' \
                '</html>\n'

        expected = '<!DOCTYPE html>\n' \
                   '<html>\n' \
                   '   <body>\n' \
                   '       <div>\n' \
                   '           <img src="images/cat.jpg" />\n' \
                   '           <img src="images/dog.jpg" />\n' \
                   '           <img src="images/rabbit.jpg" />\n' \
                   '       </div>\n' \
                   '   </body>\n' \
                   '</html>\n'
        result = render_obj1(input, 'Emil', ['cat', 'dog', 'rabbit'])
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

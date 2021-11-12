import re
import unittest

from crablib.html import generate_html, ArgNotFoundError

arguments = {'istrue': True}


def replace_if(matchobj: re.Match) -> str:
    content = matchobj.groupdict()['content']
    condition = matchobj.groupdict()['condition']
    op = matchobj.groupdict()['not']

    if op:
        condition = not condition

    if condition not in arguments:
        raise ArgNotFoundError(condition)

    if arguments[condition]:
        return content

    else:
        return ''


class TestRequest(unittest.TestCase):

    def test_no_body(self):
        input = '<!DOCTYPE html>\n' \
                '<html>\n' \
                '   <body>\n' \
                '       <div>\n' \
                '           Hi {{ name }}!\n' \
                '           {% for image in images %}\n' \
                '               {{ image }}\n' \
                '           {% endfor %}\n' \
                '       </div>\n' \
                '   </body>\n' \
                '</html>\n'

        expected = '<!DOCTYPE html>\n' \
                   '<html>\n' \
                   '   <body>\n' \
                   '       <div>\n' \
                   '            Hi Emil!' \
                   '                    cat\n' \
                   '            dog\n' \
                   '            rabbit\n' \
                   '       </div>\n' \
                   '   </body>\n' \
                   '</html>\n'
        result = generate_html(input, {'name': 'Emil', 'images': ['cat', 'dog', 'rabbit']})
        self.assertEqual(expected, result)

    def test_if(self):
        input = '<!DOCTYPE html>\n' \
                '<html>\n' \
                '   <body>\n' \
                '       <div>\n' \
                '           {% if istrue %}\n' \
                '               Hi!\n' \
                '           {% endif %}\n' \
                '       </div>\n' \
                '   </body>\n' \
                '</html>\n'

        expected = '<!DOCTYPE html>\n' \
                   '<html>\n' \
                   '   <body>\n' \
                   '       <div>\n' \
                   '           Hi!\n' \
                   '       </div>\n' \
                   '   </body>\n' \
                   '</html>\n'
        result = generate_html(input, {'istrue': True})
        print(result)
        self.assertEqual(expected, result)

    def test_something(self):
        conditionals = re.compile('{%\\s*if\\s(?P<not>not)?\\s*'
                                  '(?P<condition>\\w+)\\s*%}[\n\\s]*'
                                  '(?P<content>.+?)[\n]*{%\\s*endif\\s*%}', re.DOTALL)
        input = '<!DOCTYPE html>\n' \
                '<html>\n' \
                '   <body>\n' \
                '       <div>\n' \
                '           {% if istrue %}\n' \
                '               Hi!\n' \
                '           {% endif %}\n' \
                '       </div>\n' \
                '   </body>\n' \
                '</html>\n'

        print(conditionals.sub(replace_if, input))
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()

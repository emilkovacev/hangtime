import re


class ArgNotFoundError(Exception):
    """
    value not defined in arguments
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{{ ' + str(self.value) + ' }} not defined in arguments'


def generate_html(path: str, arguments: {str: any}) -> str:
    replace = re.compile("({{)[^(}})]+(}})")
    instance = re.compile("(?<=({{)).+(?=(}}))")
    comment = re.compile("^(<!--)[^-]*(-->)")

    def replace_str(s):
        value = instance.search(s.group(0)).group(0).strip()
        if value not in arguments:
            raise ArgNotFoundError(value)
        return str(arguments[value])

    html = ''
    with open(path, 'r') as f:
        for line in f:
            if not comment.search(line):
                html += (re.sub(replace, replace_str, line))

    return html


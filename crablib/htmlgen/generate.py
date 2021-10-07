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

    find_loops = re.compile("{%\\s+for\\s+(?P<var>\\w+)\\s+in\\s+(?P<argument>\\w+)\\s+%}"  # loop header
                            "[\n]*(?P<content>.+?)[\n]*"  # loop content
                            "{%\\s+endfor\\s+%}",  # loop end
                            re.DOTALL)

    def replace_str(s):
        value = instance.search(s.group(0)).group(0).strip()
        if value not in arguments:
            raise ArgNotFoundError(value)
        return str(arguments[value])

    def handle_loop(s):
        retval = ''
        var = s.group(1)
        arg = s.group(2)
        content = s.group(3)

        if arg not in arguments:
            raise ArgNotFoundError(arg)

        for i in arguments[arg]:
            arguments[var] = i
            retval += re.sub(replace, replace_str, content)

        return retval

    html_return = ''
    with open(path, 'r') as f:
        file = f.read()
        html = re.sub(find_loops, handle_loop, file)
        for line in html.split('\n'):
            if not comment.search(line):
                html_return += (re.sub(replace, replace_str, line)).strip(' ')

    return html_return.rstrip('\n')

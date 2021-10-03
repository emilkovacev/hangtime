import re
from .generate import ArgNotFoundError


def generate_loops(path: str, arguments: {str: any}):
    find_loops = re.compile("{%\\s+for\\s+(?P<var>\\w+)\\s+in\\s+(?P<argument>\\w+)\\s+%}"  # loop header
                            "[\n]*(?P<content>.+?)[\n]*"                          # loop content
                            "{%\\s+endfor\\s+%}",                                           # loop end
                            re.DOTALL)
    replace = re.compile("({{)[^(}})]+(}})")
    instance = re.compile("(?<=({{)).+(?=(}}))")
    comment = re.compile("^(<!--)[^-]*(-->)")

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

    with open(path, 'r') as f:
        file = f.read()
        return re.sub(find_loops, handle_loop, file)

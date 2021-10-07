import re
from crablib.texthandler.html_escape import parse_text


def read_query(query: str) -> {str: str}:
    retval = {}
    arguments = re.compile("(?<=\\?).+")
    search = arguments.search(query)

    if not search:
        return None

    for arg in search.group(0).split('&'):
        arg = arg.split('=')
        if arg[1].count('+') > 0:
            retval[arg[0]] = [parse_text(x) for x in arg[1].split('+')]
        else:
            retval[arg[0]] = parse_text(arg[1])

    return retval

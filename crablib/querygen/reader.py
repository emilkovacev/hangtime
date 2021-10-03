import re


def read(query: str) -> {str: str}:
    retval = {}
    arguments = re.compile("(?<=\\?).+")
    for arg in arguments.search(query).group(0).split('&'):
        arg = arg.split('=')
        if arg[1].count('+') > 0:
            retval[arg[0]] = arg[1].split('+')
        else:
            retval[arg[0]] = arg[1]

    return retval

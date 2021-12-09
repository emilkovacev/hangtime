import re
from typing import Dict, Any

from .error import ArgNotFoundError


loops = re.compile('{%\\s*(?P<exp>\\w+)\\s(?P<var>\\w+)\\sin\\s(?P<arg>\\w+)\\.(?P<attribute>\\w+)\\s*%}[\n]*'
                   '(?P<content>.*?)[\n\\s]*{%\\s*endfor\\s*%}')


def replace_loop(matchobj: re.Match, arguments: Dict[str, Any]) -> str:
    retval = ''
    var = matchobj.groupdict()['var']
    arg = matchobj.groupdict()['arg']
    content = matchobj.groupdict()['content']
    attribute = matchobj.groupdict()['attribute']

    if arg not in arguments:
        # raise ArgNotFoundError(arg)
        return ''

    if type(arguments[arg]) == str:
        argval = arguments[arg]
        if attribute:
            argval = argval.__dict__[attribute]
        arguments[var] = argval
        retval += content + '\n'
    else:
        for i in arguments[arg]:
            argval = arguments[i]
            if attribute:
                argval = argval.__dict__[attribute]
            arguments[var] = argval
            retval += content + '\n'

    return retval
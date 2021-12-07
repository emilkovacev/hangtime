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

    if arg not in arguments:
        raise ArgNotFoundError(arg)

    if type(arguments[arg]) == str:
        arguments[var] = arguments[arg]
        retval += variables.sub(replace_var, content) + '\n'
    else:
        for i in arguments[arg]:
            arguments[var] = i
            retval += variables.sub(replace_var, content) + '\n'

    return retval

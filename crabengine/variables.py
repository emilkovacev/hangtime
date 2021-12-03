import re
from typing import Dict, Any

from .error import ArgNotFoundError

variables = re.compile('{{\\s*(?P<var>\\w+)\\s*}}')

def replace_var(matchobj: re.Match, arguments: Dict[str, Any]) -> str:
    var = matchobj.groupdict()['var']

    if var in arguments:
        return arguments[var]
    else:
        # raise ArgNotFoundError(var)
        return ''

import re
from typing import Any, Dict

from .error import ArgNotFoundError


conditionals = re.compile('{%\\s*if.+?{%\\s*endif\\s*%}', re.DOTALL)
parse_conditions = re.compile('{%\\s*(?P<statement>if|elif|else)\\s*(?P<not>not)?\\s*'
                              '(?P<condition>\\w*)\\s*%}(?P<content>.+?)(?={%\\s*(elif|else|endif).+%})', re.DOTALL)


def replace_if(matchobj: re.Match, arguments: Dict[str, Any]) -> str:
    steps = parse_conditions.finditer(matchobj.group())
    step: re.Match
    for step in steps:
        statement = step.groupdict()['statement']
        _not = step.groupdict()['not']
        condition = step.groupdict()['condition']
        content = step.groupdict()['content']

        if statement == 'else':
            return content
        elif condition not in arguments:
            # raise ArgNotFoundError
            continue

        condition = arguments[condition]
        if _not:
            condition = not condition
        if condition:
            return content
    return ''

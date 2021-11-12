import re
from typing import Dict, List, Any

loops = re.compile('{%\\s*(?P<exp>\\w+)\\s(?P<var>\\w+)\\sin\\s(?P<arg>\\w+)\\s*%}[\n]*'
                   '(?P<content>.*?)[\n\\s]*{%\\s*endfor\\s*%}')

conditionals = re.compile('{%\\s*if\\s(?P<not>not)?\\s*(?P<condition>\\w+)\\s*%}[\n]+'
                          '(?P<content>.+?)[\n\\s]*{%\\s*endif\\s*%}', re.DOTALL)

variables = re.compile('{{\\s*(?P<var>\\w+)\\s*}}')

def generate_html(html: str, arguments: Dict[str, Any]):
    def replace_var(matchobj: re.Match) -> str:
        var = matchobj.groupdict()['var']

        if var in arguments:
            return arguments[var]
        else:
            raise ArgNotFoundError(var)

    def replace_if(matchobj: re.Match) -> str:
        content = matchobj.groupdict()['content']
        condition = matchobj.groupdict()['condition']
        op = matchobj.groupdict()['not']

        if condition not in arguments:
            raise ArgNotFoundError(condition)

        condition = arguments[condition]
        if op:
            condition = not condition

        if condition:
            return content

        else:
            return ''

    def replace_loop(matchobj: re.Match) -> str:
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

    repl_loops = loops.sub(replace_loop, html)
    repl_condition = conditionals.sub(replace_if, repl_loops)
    repl_var = variables.sub(replace_var, repl_condition)  # replace variables

    return repl_var


class ArgNotFoundError(Exception):
    """
    value not defined in arguments
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{{ ' + str(self.value) + ' }} not defined in arguments'

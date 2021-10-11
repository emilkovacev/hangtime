from crablib.querygen.reader import Query
import re

loops = re.compile('{%\\s*(?P<exp>\\w+)\\s(?P<var>\\w+)\\sin\\s(?P<arg>\\w+)\\s*%}[\n]*'
                   '(?P<content>.+?)[\n\\s]*{%\\s*endfor\\s*%}')

variables = re.compile('{{\\s+(?P<var>\\w+)\\s+}}')


def generate_html(html: str, query: Query):
    def replace_var(matchobj: re.Match) -> str:
        var = matchobj.groupdict()['var']
        if var in query.arguments:
            return query.arguments[var]
        else:
            raise ArgNotFoundError(var)

    def replace_loop(matchobj: re.Match) -> str:
        retval = ''
        var = matchobj.groupdict()['var']
        arg = matchobj.groupdict()['arg']
        content = matchobj.groupdict()['content']

        if arg not in query.arguments:
            raise ArgNotFoundError(arg)

        if arg in query.single:
            query.arguments[var] = query.arguments[arg]
            retval += variables.sub(replace_var, content) + '\n'
        else:
            for i in query.arguments[arg]:
                query.arguments[var] = i
                retval += variables.sub(replace_var, content) + '\n'

        return retval

    repl_loops = loops.sub(replace_loop, html)
    repl_var = variables.sub(replace_var, repl_loops)  # replace variables

    return repl_var


class ArgNotFoundError(Exception):
    """
    value not defined in arguments
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{{ ' + str(self.value) + ' }} not defined in arguments'

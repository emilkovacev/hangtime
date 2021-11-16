from typing import Dict, Any
from functools import partial

from .conditionals import conditionals, replace_if
from .loops import loops, replace_loop
from .variables import variables, replace_var


def generate_html(html: str, arguments: Dict[str, Any]):
    # partial() is used to pass arguments to replacement functions
    html = loops.sub(partial(replace_loop, arguments=arguments), html)          # replace loops
    html = conditionals.sub(partial(replace_if, arguments=arguments), html)     # replace conditionals
    html = variables.sub(partial(replace_var, arguments=arguments), html)       # replace variables

    return html

from typing import Callable

from crablib.http.parse import Request


class Path:
    def __init__(self, regex: str, view: Callable[[Request], bytes]):
        self.regex = regex
        self.view = view

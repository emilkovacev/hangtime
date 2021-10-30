from typing import Callable, Any
from socketserver import BaseRequestHandler

from crablib.http.parse import Request


class Path:
    def __init__(self, regex: str, view: Callable[[Any, Request], None]):
        self.regex = regex
        self.view = view

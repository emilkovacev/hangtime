import re
from typing import Dict, Any

from crablib.html import generate_html


class FileIO:
    def __init__(self, path):
        self.path = path
        self.extension = self.find_extension()

    def find_extension(self) -> str:
        match = re.search('(?<=\\.)[^.]+$', self.path)
        if match:
            return match.group(0)
        else:
            return ''

    def read(self, arguments=None) -> bytes:
        ext = self.extension
        if ext == 'html' and arguments:
            with open(self.path, 'r') as f:
                return generate_html(f.read(), arguments).encode()

        else:
            with open(self.path, 'rb') as f:
                return f.read()

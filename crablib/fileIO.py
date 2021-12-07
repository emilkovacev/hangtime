import re
from os import path as ospath

from crabengine.generate import generate_html


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
        path = ospath.relpath(self.path)
        if ext == 'html' and arguments:
            with open(path, 'r') as f:
                return generate_html(f.read(), arguments).encode()

        else:
            with open(path, 'rb') as f:
                return f.read()

    def read_template(self, arguments=None) -> bytes:
        path = ospath.relpath(self.path)
        if not arguments:
            arguments = {}

        with open(path, 'r') as f:
            return generate_html(f.read(), arguments).encode()
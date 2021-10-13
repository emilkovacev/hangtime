import re

from crablib.htmlgen.generate import generate_html


class FileIO:
    def __init__(self, path, query=None):
        self.path = path
        self.query = query
        self.extension = self.find_extension()

    def find_extension(self) -> str:
        match = re.search('(?<=\\.)[^.]+$', self.path)
        if match:
            return match.group(0)
        else:
            return ''

    def read(self) -> bytes:
        ext = self.extension
        if ext == 'html' and self.query and self.query.isvalid():
            with open(self.path, 'r') as f:
                return generate_html(f.read(), self.query).encode()

        else:
            with open(self.path, 'rb') as f:
                return f.read()

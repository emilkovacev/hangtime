from crablib.http.parse import FileIO
from crablib.querygen.reader import read_query


class Path:
    def __init__(self, regex: str, mimetype: str, path: str = None):
        self.regex = regex
        self.mimetype = mimetype
        self.path = path

    def retval(self) -> bytes:
        if self.path:
            return FileIO(self.path, read_query(self.path)).read()

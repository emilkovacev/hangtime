from pathlib import Path


class PathIter:
    def __init__(self, path):
        self.path = Path(path)
        self.files = [file for file in path if not file.is_dir()]

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.files) == 0:
            raise StopIteration
        return self.files.pop()


def image_type(path: str) -> str:
    if '/' in path:
        i = path.split('/')[-1]
        if '.' in i:
            return 'file'

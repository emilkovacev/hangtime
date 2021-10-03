import re


def generate_loops(path: str, arguments: {str: any}):
    find_loops = re.compile("({%.+%})$", re.MULTILINE)
    with open(path, 'r') as f:
        file = f.read()
        print(find_loops.split(file))

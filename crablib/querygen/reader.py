import re
from crablib.texthandler.html_escape import parse_text


class Query:
    def __init__(self, query: str, arguments: {str: str}, single=None):
        self.query = query
        self.arguments: {str: str} = arguments
        self.single = single

    def images(self):
        if self.arguments and 'images' in self.arguments:
            if 'images' in self.single:
                self.arguments['images'] = '/images/' + self.arguments['images'] + '.jpg'
            else:
                new = []
                for name in self.arguments['images']:
                    new.append('/images/' + name + '.jpg')
                self.arguments['images'] = new
        return self

    def isvalid(self):
        return self.arguments


def read_query(query: str) -> Query:
    retval = {}
    single = set()
    arguments = re.compile("(?<=\\?).+")
    search = arguments.search(query)

    if not search:
        return Query(query, None)

    for arg in search.group(0).split('&'):
        arg = arg.split('=')
        if arg[1].count('+') > 0:
            retval[arg[0]] = [parse_text(x) for x in arg[1].split('+')]
        else:
            retval[arg[0]] = parse_text(arg[1])
            single.add(arg[0])

    q = Query(query, retval, single)
    return q

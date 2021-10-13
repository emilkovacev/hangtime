import re
from typing import List, Dict, Iterator, Tuple

from crablib.http.response import http_200, http_301
from crablib.http.parse import Request, parse_header, Header, escape
from crablib.fileIO import FileIO


# text/html
data: List[str] = []
def index(request: Request) -> bytes:
    return http_200(
        content_type='text/html',
        content=FileIO('html/index.html').read({'messages': data})
    ).write_raw()


def yoshi(request: Request) -> bytes:
    return http_200(
        content_type='text/html',
        content=FileIO('html/yoshi.html').read()
    ).write_raw()


def images(request: Request) -> bytes:
    retval = {}
    arguments = re.compile("(?<=\\?).+")
    search = arguments.search(request.path)

    for arg in search.group(0).split('&'):
        arg = arg.split('=')
        if arg[1].count('+') > 0:
            if arg[0] == 'images':
                retval[arg[0]] = [f'images/{x}.jpg' for x in arg[1].split('+')]
            else:
                retval[arg[0]] = [x for x in arg[1].split('+')]
        else:
            if arg[0] == 'images':
                retval[arg[0]] = f'images/{arg[1]}.jpg'
            else:
                retval[arg[0]] = arg[1]

    return http_200(
        content_type='text/html',
        content=FileIO('html/images.html').read(retval)
    ).write_raw()


# text/css
def css(request: Request) -> bytes:
    return http_200(
        content_type='text/css',
        content=FileIO('style/style.css').read()
    ).write_raw()


# script/js
def js(request: Request) -> bytes:
    return http_200(
        content_type='text/javascript',
        content=FileIO('script/script.js').read()
    ).write_raw()


# image/jpg
def img(request: Request) -> bytes:
    return http_200(
        content_type='image/jpeg',
        content=FileIO(request.path.lstrip('/')).read()
    ).write_raw()


# forms
def form(request: Request) -> bytes:

    boundary: str = '--' + re.search('boundary=(?P<boundary>.+);?', request.headers['Content-Type']).group(1)
    bytesearch = boundary.encode() + b'\r\n(?P<headers>.+)\r\n\r\n(?P<content>.+)\r\n'
    content_chunks: List[re.Match] = re.findall(bytesearch, request.body)

    retval: Dict[str, bytes] = {}
    content: Tuple[bytes]
    for content in content_chunks:
        headers: List[str] = content[0].decode().split('\r\n')
        headers_dict: Dict[str, Header] = {}
        for header in headers:
            headerobj: Header = parse_header(header)
            print(headerobj.name)
            headers_dict[headerobj.name] = headerobj
        content_name: str = headers_dict['Content-Disposition'].options['name']
        retval[content_name] = content[1]
        data.append(escape(f'{content_name}: {content[1].decode()}'))

    print(data)
    response: bytes = http_301('/').write_raw()
    return response

import re

from crablib.http.response import http_200
from crablib.http.parse import Request
from crablib.fileIO import FileIO


# text/html
def index(request: Request) -> bytes:
    return http_200(
        content_type='text/html',
        content=FileIO('html/index.html').read()
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

# data: [{str: str}] = []
# def form(request: Request) -> bytes:
#     return http_200(
#         content_type='text/html',
#         content=FileIO('html/index.html', arglist).read()
#     ).write_raw()

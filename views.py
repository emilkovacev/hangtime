import json

from crablib.http.parse import Request, FileIO
from crablib.http.response import http_200
from crablib.querygen.reader import Query, read_query


# text/html

def index(request: Request) -> bytes:
    query: Query = read_query(request.path).images()
    return http_200(
        content_type='text/html',
        content=FileIO('html/index.html', query).read()
    ).write_raw()


def yoshi(request: Request) -> bytes:
    query: Query = read_query(request.path).images()
    return http_200(
        content_type='text/html',
        content=FileIO('html/yoshi.html', query).read()
    ).write_raw()


def images(request: Request) -> bytes:
    query: Query = read_query(request.path).images()
    return http_200(
        content_type='text/html',
        content=FileIO('html/images.html', query).read()
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

data: [{str: str}] = []


def form(request: Request) -> bytes:
    data.append(request.parse_form())
    print(request.parse_form())
    print(data)
    arglist = Query(query='', arguments={'messages': [f'{x[0]}: {x[1]}' for x in data]})

    return http_200(
        content_type='text/html',
        content=FileIO('html/index.html', arglist).read()
    ).write_raw()

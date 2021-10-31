from crablib.fileIO import FileIO
from crablib.http.parse import Request
from crablib.http.response import InvalidRequest
from crablib.http.response import http_200


def index(socket, request: Request) -> None:
    if request.request_type == 'GET':
        response = http_200(
            content_type='text/html',
            content=FileIO('html/index.html').read(),
            charset='utf-8'
        ).write_raw()
        socket.request.sendall(response)

    else:
        raise InvalidRequest


def yoshi(socket, request: Request) -> None:
    if request.request_type == 'GET':
        response = http_200(
            content_type='text/html',
            content=FileIO('html/yoshi.html').read(),
            charset='utf-8'
        ).write_raw()

        socket.request.sendall(response)

    else:
        raise InvalidRequest


# text/css
def css(socket, request: Request) -> None:
    if request.request_type == 'GET':
        response =  http_200(
            content_type='text/css',
            content=FileIO('style/style.css').read(),
            charset='utf-8'
        ).write_raw()

        socket.request.sendall(response)

    else:
        raise InvalidRequest


# script/js
def js(socket, request: Request) -> None:
    if request.request_type == 'GET':
        response = http_200(
            content_type='text/javascript',
            content=FileIO('script/script.js').read()
        ).write_raw()

        socket.request.sendall(response)

    else:
        raise InvalidRequest


# image/jpg
def img(socket, request: Request) -> None:
    if request.request_type == 'GET':
        response = http_200(
            content_type='image/jpeg',
            content=FileIO(request.path.lstrip('/')).read()
        ).write_raw()

        socket.request.sendall(response)

    else:
        raise InvalidRequest

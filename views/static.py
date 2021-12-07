import bcrypt

from crablib.fileIO import FileIO
from crablib.http.parse import Request
from crablib.http.response import InvalidRequest, http_301
from crablib.http.response import http_200
from crablib.auth import get_request_account
from db.account import get_account_from_token


def index(socket, request: Request) -> None:
    if request.request_type == 'GET':
        account = get_request_account(request)
        if account:
            username = account['username']
            response = http_200('text/html', FileIO('html/calendar.html').read({'username': username}))
            return socket.request.sendall(response.write_raw())

        response = http_301('/login')
        return socket.request.sendall(response.write_raw())

    else:
        raise InvalidRequest


# text/css
def css(socket, request: Request) -> None:
    path = request.path.split('/style/')[1]
    if request.request_type == 'GET':
        response = http_200(
            content_type='text/css',
            content=FileIO(f'style/{path}').read(),
            charset='utf-8'
        ).write_raw()

        socket.request.sendall(response)

    else:
        raise InvalidRequest


# script/js
def js(socket, request: Request) -> None:
    path = request.path.split('/script/')[1]
    if request.request_type == 'GET':
        response = http_200(
            content_type='text/javascript',
            content=FileIO(f'script/{path}').read()
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

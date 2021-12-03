import bcrypt

from crablib.fileIO import FileIO
from crablib.http.parse import Request
from crablib.http.response import InvalidRequest, http_301
from crablib.http.response import http_200
from db.account import get_account_from_token


def index(socket, request: Request) -> None:
    if request.request_type == 'GET':
        if request.cookies and 'auth_token' in request.cookies:
            salt = b'$2b$12$Fr9yR03IQLCGqjB1MJ9gfu'
            auth_token_hash: str = bcrypt.hashpw(request.cookies['auth_token'].encode(), salt).decode()
            account = get_account_from_token(auth_token_hash)

            if account and account['auth_token_hash'] == auth_token_hash:
                username = account['username']
                return socket.request.sendall(http_200('text/simple', f'welcome back {username}!'.encode()).write_raw())

        response = http_301('/login')
        return socket.request.sendall(response.write_raw())

    else:
        raise InvalidRequest


# text/css
def css(socket, request: Request) -> None:
    if request.request_type == 'GET':
        response = http_200(
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

from typing import List, Dict

from crablib.fileIO import FileIO
from crablib.http.parse import Request, Cookie, parse_cookie, Response
from crablib.http.response import InvalidRequest
from crablib.http.response import http_200


def index(socket, request: Request) -> None:
    if request.request_type == 'GET':
        page_visits_cookie = None

        if 'Cookie' not in request.headers:
            cookie = Cookie(
                name='page-visits',
                value=str(1),
                max_age=str(7200),
                secure=False,
            )
            page_visits_cookie = cookie

        else:
            cookies: Dict[str, Cookie] = parse_cookie(request.headers['Cookie'])
            if 'page-visits' in cookies:
                updated_cookie = cookies['page-visits']
                updated_cookie.value = str(int(updated_cookie.value) + 1)
                page_visits_cookie = updated_cookie

        response: Response = http_200(
            content_type='text/html',
            content=FileIO('html/index.html').read({'page_visits': page_visits_cookie.value}),
            charset='utf-8',
        )

        response.add_cookie(page_visits_cookie)
        socket.request.sendall(response.write_raw())

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

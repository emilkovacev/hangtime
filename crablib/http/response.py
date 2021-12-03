from typing import Dict, Tuple, List

from crablib.http.parse import Response, Cookie
from crablib.http.websocket import generate_key


class InvalidRequest(Exception):
    """
    Request has invalid parameters
    """


def http_200(content_type: str, content: bytes, charset: str = None, cookies: List[Cookie] = None) -> Response:
    headers = {
        'Content-Type': content_type,
        'Content-Length': len(content.strip()),
        'X-Content-Type-Options': 'nosniff',
    }

    if charset:
        headers['Content-Type'] += f'; charset={charset}'

    if cookies:
        headers['Set-Cookie'] = cookies

    response = Response(
        status_code=200,
        status_message='OK',
        headers=headers,
        body=content,
    )

    return response


def http_301(path: str) -> Response:
    response = Response(
        status_code=301,
        status_message='Moved Permanently',
        headers={
            'Location': path,
            'Content-Length': 0,
        },
    )
    return response


def http_403(content_type: str, content: bytes) -> Response:
    response = Response(
        status_code=403,
        status_message='Forbidden Response',
        headers={
            'Content-Type': content_type,
            'Content-Length': len(content.strip()),
        },
    )
    return response


def http_404(content_type: str, content: bytes) -> Response:
    response = Response(
        status_code=404,
        status_message='Not Found',
        headers={
            'Content-Type': content_type,
            'Content-Length': len(content.strip()),
        },
        body=content,
    )
    return response


def handshake_response(websocket_key: str) -> Response:
    response = Response(
        status_code=101,
        status_message='Switching Protocols',
        headers={
            'Connection': 'Upgrade',
            'Upgrade': 'websocket',
            'Sec-WebSocket-Accept': generate_key(websocket_key)
        },
    )
    return response


def http_201(data: bytes):
    response = Response(
        status_code=201,
        status_message='Created',
        headers={
            'Content-Type': 'text/plain',
            'Content-Length': len(data),
            'X-Content-Type-Options': 'nosniff',
        },
        body=data
    )
    return response

def http_204():
    response = Response(
        status_code=201,
        status_message='No Content',
        headers={
            'Content-Type': 'text/plain',
            'Content-Length': 0,
            'X-Content-Type-Options': 'nosniff',
        },
    )
    return response



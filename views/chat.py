import re

from crablib.fileIO import FileIO
from crablib.http.parse import Request, Response
from crablib.http.response import http_200, http_404
from crablib.http.websocket import generate_key

def websocket(request: Request) -> bytes:
    if request.request_type == 'GET':
        response = Response(
            status_code=101,
            status_message='Switching Protocols',
            headers={
                'Connection': 'Upgrade',
                'Upgrade': 'websocket',
                'Sec-WebSocket-Accept': generate_key(request.headers['Sec-WebSocket-Key'])
            },
        ).write_raw()
        return response
    return http_404(
        content_type='text/html',
        content=FileIO('html/404.html').read()
    ).write_raw()

def websocketjs(request: Request) -> bytes:
    return http_200(
        content_type='text/javascript',
        content=FileIO('script/websocket.js').read()
    ).write_raw()

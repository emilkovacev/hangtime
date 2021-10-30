from socketserver import BaseRequestHandler

from crablib.fileIO import FileIO
from crablib.http.parse import Request, Response, parse_frame, Frame
from crablib.http.response import http_200, handshake_response, InvalidRequest

import json


def websocket(socket, request: Request) -> None:
    if request.request_type == 'GET':
        socket.clients.append(socket)
        key = request.headers['Sec-WebSocket-Key']
        response = handshake_response(key).write_raw()
        socket.request.sendall(response)

        while True:
            raw: bytes = socket.request.recv(2048)
            frame: Frame = parse_frame(raw)
            if frame.opcode == 8: break
            # socket.request.sendall(frame.write_raw())

            # ------------these lines crash ---------------
            for client in socket.clients:
                client.request.sendall(frame.write_raw())
            # ---------------------------------------------

    else:
        raise InvalidRequest

def websocketjs(socket, request: Request) -> None:
    if request.request_type == 'GET':
        response = http_200(
            content_type='text/javascript',
            content=FileIO('script/websocket.js').read()
        ).write_raw()

        socket.request.sendall(response)

    else:
        raise InvalidRequest

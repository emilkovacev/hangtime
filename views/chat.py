from crablib.fileIO import FileIO
from crablib.http.parse import Request, parse_frame, Frame
from crablib.http.response import http_200, handshake_response, InvalidRequest
from db import messages
import json


def index(socket, request: Request):
    if request.request_type == 'GET':

        response = http_200(
            content_type='text/html',
            content=FileIO('html/chat.html').read(),
            charset='utf-8',
        )

        socket.request.sendall(response.write_raw())

    else:
        raise InvalidRequest


def load_prev_messages(socket):
    for data in messages.get_messages():
        message: str = json.dumps({'username': data['username'], 'comment': data['comment']})
        message_frame = Frame(
            FIN=1, RSV1=0, RSV2=0, RSV3=0,
            opcode=1, payload_len=len(message), MASK=0, data=message.encode()
        )
        try:
            socket.request.sendall(message_frame.write_raw())
        except OSError:
            pass


def load_message(socket):
    while True:
        raw: bytes = socket.request.recv(2048)
        frame: Frame = parse_frame(raw)
        if frame.opcode == 8: break                                 # end websocket connection

        data = json.loads(frame.data)
        messages.create_message(username=data['username'], comment=data['comment'])  # store message in db

        for client in socket.clients:                               # send message to each connected client
            try:
                client.request.sendall(frame.write_raw())
            except OSError:
                pass


def websocket(socket, request: Request) -> None:
    if request.request_type == 'GET':
        # implement websocket handshake
        socket.clients.append(socket)
        key = request.headers['Sec-WebSocket-Key']
        response = handshake_response(key).write_raw()
        socket.request.sendall(response)

        load_prev_messages(socket)  # load messages sent before user loaded
        load_message(socket)        # load any messages sent while websocket is open

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

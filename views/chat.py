from crablib.fileIO import FileIO
from crablib.http.parse import Request, Response, parse_frame, Frame
from crablib.http.response import http_200, handshake_response, InvalidRequest
import messages
import json


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


def websocket(socket, request: Request) -> None:
    if request.request_type == 'GET':
        socket.clients.append(socket)
        key = request.headers['Sec-WebSocket-Key']
        response = handshake_response(key).write_raw()
        socket.request.sendall(response)

        load_prev_messages(socket)

        while True:
            raw: bytes = socket.request.recv(2048)
            frame: Frame = parse_frame(raw)
            if frame.opcode == 8: break

            data = json.loads(frame.data)
            messages.create_message(data['username'], data['comment'])

            for client in socket.clients:
                try:
                    client.request.sendall(frame.write_raw())
                except OSError:
                    pass

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

import bcrypt
import sys

from crablib.fileIO import FileIO
from crablib.http.parse import Request, parse_frame, Frame
from crablib.http.response import http_200, handshake_response, InvalidRequest
from crablib.auth import get_request_account
from db import messages
from db import account as acc
import json

from db.account import get_account_from_token


def index(socket, request: Request):
    account = get_request_account(request)
    if request.request_type == 'GET' and account:
        users = [a['username'] for a in acc.get_accounts({'status': 'online'})]
        users.remove(account['username'])
        response = http_200(
            content_type='text/html',
            content=FileIO('html/chat.html').read({'users': users, 'username': account['username']}),
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


def load_message(socket, username):
    while True:
        raw: bytes = socket.request.recv(2048)
        frame: Frame = parse_frame(raw)
        if frame.opcode == 8: break                                 # end websocket connection

        data = json.loads(frame.data)
        #messages.create_message(username=data['username'], comment=data['comment'])  # store message in db

        if data['username'] in socket.chatclients:
            framedict = {
                "username": username,
                "comment": data['comment']
            }
            framejson = json.dumps(framedict).encode()
            sendframe = Frame(FIN=1, RSV1=0, RSV2=0, RSV3=0, opcode=1, MASK=0,data=framejson, payload_len=len(framejson))
            socket.request.sendall(sendframe.write_raw())
            for client in socket.chatclients[data['username']]:  # send message to each connected client
                try:
                    client.request.sendall(sendframe.write_raw())
                except OSError:
                    pass



def websocket(socket, request: Request) -> None:
    print(f'websocket headers: {request.headers}')
    sys.stdout.flush()
    if request.request_type == 'GET':
        # implement websocket handshake
        auth_token = request.cookies['auth_token']
        auth_token_salt = b'$2b$12$Fr9yR03IQLCGqjB1MJ9gfu'
        auth_token_hash = bcrypt.hashpw(auth_token.encode(), auth_token_salt).decode()
        username = get_account_from_token(auth_token_hash)["username"]
        if username in socket.chatclients:
            socket.chatclients[username].append(socket)
        else:
            socket.chatclients[username] = [socket]

        key = request.headers.get('Sec-WebSocket-Key', request.headers['Sec-Websocket-Key'])
        response = handshake_response(key).write_raw()
        socket.request.sendall(response)

        #load_prev_messages(socket)  # load messages sent before user loaded
        load_message(socket, username)        # load any messages sent while websocket is open

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

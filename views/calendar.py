import json
import time
from datetime import datetime, timedelta

from crablib.http.parse import Request, parse_form, Frame, parse_frame
from crablib.http.response import http_301, InvalidRequest, handshake_response
from db.events import create_event, all_events, dict_event
from crablib.misc import flush_print


def event_validate(event):
    #print("validating", event)
    start = datetime.strptime(event["starttime"], '%H:%M').time()
    end = datetime.strptime(event["endtime"], '%H:%M').time()
    diff = timedelta(hours=end.hour, minutes=end.minute) - timedelta(hours=start.hour, minutes=start.minute)
    minimum = timedelta(minutes=15)
    if diff > minimum:
        return True
    else:
        return False


def event(socket, request: Request):
    if request.request_type != "POST":
        raise InvalidRequest
    if not request.body:
        request.body = socket.request.recv(int(request.headers["Content-Length"]))
    encodedict = parse_form(request)
    formdict = {}
    for key in encodedict:
        formdict[key] = encodedict[key].decode("ascii")
    #print("formdict", formdict)
    if event_validate(formdict):
        create_event(formdict["event-name"], formdict["description"], formdict["starttime"], formdict["endtime"], formdict["color"])
        event = dict_event(formdict["event-name"], formdict["description"], formdict["starttime"], formdict["endtime"], formdict["color"])
        for client in socket.clients:
            frame = create_frame(event)
            send_frame(client, frame)
    response = http_301("/")
    socket.request.sendall(response.write_raw())


def websocket(socket, request: Request) -> None:
    if request.request_type == 'GET':
        # implement websocket handshake
        key = request.headers.get('Sec-WebSocket-Key', request.headers['Sec-Websocket-Key'])
        response = handshake_response(key).write_raw()
        socket.request.sendall(response)
        socket.clients.append(socket)
        allevents = all_events()
        for events in allevents:
            frame = create_frame(events)
            send_frame(socket, frame)
        calsock(socket)

    else:
        raise InvalidRequest


def calsock(socket):
    while True:
        raw: bytes = socket.request.recv(2048)
        frame: Frame = parse_frame(raw)
        if frame.opcode == 8:
            socket.clients.remove(socket)
            break



def create_frame(body):
    bopy = body.copy()
    if '_id' in bopy:
        bopy.pop('_id')
    b = json.dumps(bopy)
    bencode = b.encode("ascii")
    frame = Frame(1, 0, 0, 0, 1, 0, len(bencode), bencode)
    #print(frame)
    return frame.write_raw()


def send_frame(socket, frame):
    #print("sent frame babey")
    try:
        socket.request.sendall(frame)
    except Exception:
        flush_print("you win some you lose some")


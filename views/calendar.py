import json
import time
from datetime import datetime, timedelta

from crablib.http.parse import Request, parse_form, Frame
from crablib.http.response import http_301, InvalidRequest, handshake_response
from db.events import create_event, all_events


def event_validate(event):
    # print("validating", event)
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
    encodedict = parse_form(request)
    formdict = {}
    for key in encodedict:
        formdict[key] = encodedict[key].decode("ascii")
    # print("formdict", formdict)
    if event_validate(formdict):
        create_event(
            formdict["event-name"],
            formdict["description"],
            formdict["starttime"],
            formdict["endtime"],
            formdict["color"])
    response = http_301("/")
    socket.request.sendall(response.write_raw())


def websocket(socket, request: Request) -> None:
    if request.request_type == 'GET':
        # implement websocket handshake
        socket.clients.append(socket)
        key = request.headers['Sec-WebSocket-Key']
        response = handshake_response(key).write_raw()
        socket.request.sendall(response)
        calsock(socket)

    else:
        raise InvalidRequest


def calsock(socket):
    sent = []
    while True:
        all = all_events()
        for event in all:
            if event["_id"] not in sent:
                sent.append(event["_id"])
                frame = create_frame(event)
                send_frame(socket, frame)
                # print(event)
        # time.sleep(0.5)


def create_frame(body):
    bopy = body.copy()
    bopy.pop('_id')
    b = json.dumps(bopy)
    bencode = b.encode("ascii")
    frame = Frame(1, 0, 0, 0, 1, 0, len(bencode), bencode)
    # print(frame)
    return frame.write_raw()


def send_frame(socket, frame):
    socket.request.sendall(frame)

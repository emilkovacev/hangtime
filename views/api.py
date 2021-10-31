import json
import re

from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from crablib.http.parse import Request, Response
from crablib.http.response import InvalidRequest, http_201, http_200, http_404, http_204
from db import users


def routing(socket, request: Request):
    if request.request_type == 'GET' and request.path == '/users':
        retrieve_list(socket, request)
    elif request.request_type == 'POST':
        create(socket, request)
    else:
        raise InvalidRequest


def param_routing(socket, request: Request):
    if request.request_type == 'GET':
        retrieve_single(socket, request)
    elif request.request_type == 'PUT':
        update(socket, request)
    elif request.request_type == 'DELETE':
        delete(socket, request)
    else:
        raise InvalidRequest


def get_id(path: str):
    return re.match('^/users/(?P<id>\\w+)$', path).groupdict()['id']


def create(socket, request: Request):
    data = json.loads(request.body)
    result: InsertOneResult = users.create_user(email=data['email'], username=data['username'])

    data['id'] = str(result.inserted_id)
    response: bytes = http_201(json.dumps(data).encode()).write_raw()
    socket.request.sendall(response)


def retrieve_list(socket, request: Request):
    records = [
        {
            'id': str(record['_id']),
            'email': record['email'],
            'username': record['username']
        } for record in users.get_users()
    ]

    encoded = json.dumps(records).encode()
    if len(records) == 0: encoded = b'[]'

    response: bytes = http_200('text/plain', encoded).write_raw()
    socket.request.sendall(response)


def retrieve_single(socket, request: Request):
    user_id = get_id(request.path)
    user = users.get_single_user(user_id)
    user['_id'] = str(user['_id'])

    encoded = json.dumps(user).encode()
    response: bytes = http_201(encoded).write_raw()
    socket.request.sendall(response)


def update(socket, request: Request):
    user_id = get_id(request.path)
    parsed = json.loads(request.body)
    parsed['id'] = user_id
    result: UpdateResult = users.update_user(
        user_id=user_id,
        email=parsed['email'],
        username=parsed['username']
    )

    if result.modified_count:
        response: bytes = http_200('text/plain', json.dumps(parsed).encode()).write_raw()
        socket.request.sendall(response)

    else:
        response: bytes = http_404('text/plain', b'Update failed').write_raw()
        socket.request.sendall(response)

def delete(socket, request: Request):
    user_id = get_id(request.path)
    result: DeleteResult = users.delete_user(user_id)

    if result.deleted_count:
        response: bytes = http_204().write_raw()
        socket.request.sendall(response)

    else:
        response: bytes = http_404('text/plain', b'Delete failed').write_raw()
        socket.request.sendall(response)
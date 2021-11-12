import re
import string
from typing import Dict, List
import bcrypt

from crablib.fileIO import FileIO
from crablib.http.parse import Request, parse_form, Response, parse_cookie, Cookie
from crablib.http.response import http_200, InvalidRequest, http_301
from db.account import create_account, get_account


def login(socket, request: Request):
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
            content=FileIO('html/login.html').read({'page_visits': page_visits_cookie.value}),
            charset='utf-8',
        )

        response.add_cookie(page_visits_cookie)
        socket.request.sendall(response.write_raw())

    elif request.request_type == 'POST':
        form: Dict[str, bytes] = parse_form(request)
        username = form['username']
        password = form['password']

        if len(username) == 0 or len(password) == 0:
            response = http_301('/login')
            socket.request.sendall(response.write_raw())
            return

        account = get_account(str(username))
        hashed = bcrypt.hashpw(password, account['salt'])
        if hashed == account['password_hash']:
            # we're good to login!
            print('successful login')
            socket.request.sendall(http_200('text/simple', b'login successful!').write_raw())
        else:
            print('failed login attempt')
            socket.request.sendall(http_200('text/simple', b'login failed :(').write_raw())

    else:
        raise InvalidRequest


def check_password(password: str) -> bool:
    conditions = [
        len(password) >= 8,
        len(re.findall('[a-z]', password)) > 1,
        len(re.findall('[A-Z]', password)) > 1,
        len(re.findall('[0-9]', password)) > 1,
        len(re.findall(f'[{string.punctuation}]', password))
    ]
    for condition in conditions:
        if not condition:
            return False
    return True


def register_response(arguments=None):
    if not arguments:
        return http_200(
            content_type='text/html',
            content=FileIO('html/register.html').read(),
            charset='utf-8',
        )
    else:
        return http_200(
            content_type='text/html',
            content=FileIO('html/register_response.html').read(arguments),
            charset='utf-8',
        )

def register(socket, request: Request):
    if request.request_type == 'GET':

        socket.request.sendall(register_response().write_raw())

    elif request.request_type == 'POST':
        form: Dict[str, bytes] = parse_form(request)
        email = form['email']
        username = form['username']
        password = form['password']
        #
        # if get_account(str(username)):
        #     socket.request.sendall(register_response({'already_taken': True, 'good_password': True}).write_raw())
        #     return
        if not check_password(str(password)):
            socket.request.sendall(register_response({'already_taken': False, 'good_password': False}).write_raw())
            return

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        create_account(str(email), str(username), hashed, salt)

        socket.request.sendall(register_response({'already_taken': False, 'good_password': True}).write_raw())

    else:
        raise InvalidRequest

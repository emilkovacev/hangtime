import re
import string
from typing import Dict, List
import bcrypt
import secrets

from crablib.fileIO import FileIO
from crablib.http.parse import Request, parse_form, Response, Cookie
from crablib.http.response import http_200, InvalidRequest, http_301
from db.account import create_account, get_account, add_token


def login(socket, request: Request):
    if request.request_type == 'GET':
        cookie = Cookie('page-visits', str(1), str(7200), secure=False)

        if 'page-visits' in request.cookies:
            cookie.value = str(int(request.cookies['page-visits']) + 1)

        arguments = {'page_visits': cookie.value}
        response: Response = http_200('text/html', FileIO('html/login.html').read(arguments), 'utf-8')

        response.add_cookie(cookie)
        socket.request.sendall(response.write_raw())

    elif request.request_type == 'POST':
        form: Dict[str, bytes] = parse_form(request)
        username = form['username'].decode()
        password = form['password']

        if len(username) == 0 or len(password) == 0:
            response = http_301('/login')
            socket.request.sendall(response.write_raw())
            return

        account = get_account(username)
        hashed = bcrypt.hashpw(password, account['salt'].encode()).decode()

        if hashed == account['password_hash']:
            # we're good to login!
            response = http_301('/')

            auth_token: str = secrets.token_urlsafe(30)
            cookie = Cookie(
                name='auth_token',
                value=auth_token,
                max_age=str(7200),
                secure=False
            )
            response.add_cookie(cookie)
            auth_token_salt = b'$2b$12$Fr9yR03IQLCGqjB1MJ9gfu'
            auth_token_hash = bcrypt.hashpw(auth_token.encode(), auth_token_salt)
            add_token(username, auth_token_hash.decode())

            print('successful login')

            socket.request.sendall(response.write_raw())
            
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
        return http_200('text/html', FileIO('html/register.html').read(), 'utf-8')
    else:
        return http_200('text/html', FileIO('html/register_response.html').read(arguments), 'utf-8')

def register(socket, request: Request):
    if request.request_type == 'GET':
        socket.request.sendall(register_response().write_raw())

    elif request.request_type == 'POST':
        form: Dict[str, bytes] = parse_form(request)
        email = form['email'].decode()
        username = form['username'].decode()
        password = form['password']
        print(password)

        if not check_password(str(password)):
            arguments = {'username_taken': False, 'good_password': False}
            socket.request.sendall(register_response(arguments).write_raw())
            return

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        account = create_account(str(email), username, hashed.decode(), salt.decode())

        if account:
            arguments = {'username_taken': False, 'good_password': True}
            socket.request.sendall(register_response(arguments).write_raw())
        else:
            arguments = {'username_taken': True, 'good_password': True}
            socket.request.sendall(register_response(arguments).write_raw())

    else:
        raise InvalidRequest

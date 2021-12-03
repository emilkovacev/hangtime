import re
import string
from typing import Dict, List
import bcrypt
import secrets

from crablib.fileIO import FileIO
from crablib.http.parse import Request, parse_form, Response, Cookie
from crablib.http.response import http_200, InvalidRequest, http_301, http_403
from db.account import create_account, get_account, add_token, get_account_from_password, get_account_from_token


def login(socket, request: Request):
    if request.request_type == 'GET':
        cookie = Cookie('page-visits', str(1), max_age=7200, secure=False)

        if 'page-visits' in request.cookies:
            cookie.value = str(int(request.cookies['page-visits']) + 1)

        arguments = {'page_visits': cookie.value}
        response: Response = http_200('text/html', FileIO('html/login.html').read(arguments), 'utf-8')

        response.add_cookie(cookie)
        return socket.request.sendall(response.write_raw())

    elif request.request_type == 'POST':
        form: Dict[str, bytes] = parse_form(request)
        username = form['username'].decode()
        password = form['password']

        if len(username) == 0 or len(password) == 0:
            response = http_301('/login')
            return socket.request.sendall(response.write_raw())

        account = get_account(username)

        if not account:
            arguments = {'username_exists': False}
            response: Response = http_200('text/html', FileIO('html/login.html').read(arguments), 'utf-8')
            return socket.request.sendall(response.write_raw())

        # ██╗░░██╗░█████╗░░██████╗██╗░░██╗░░░░░░░░░░░░░░░░░░░░░░██████╗░█████╗░██╗░░░░░████████╗
        # ██║░░██║██╔══██╗██╔════╝██║░░██║░░░░░░░░░██╗░░░░░░░░░██╔════╝██╔══██╗██║░░░░░╚══██╔══╝
        # ███████║███████║╚█████╗░███████║░░░░░░░██████╗░░░░░░░╚█████╗░███████║██║░░░░░░░░██║░░░
        # ██╔══██║██╔══██║░╚═══██╗██╔══██║░░░░░░░╚═██╔═╝░░░░░░░░╚═══██╗██╔══██║██║░░░░░░░░██║░░░
        # ██║░░██║██║░░██║██████╔╝██║░░██║░░░░░░░░░╚═╝░░░░░░░░░██████╔╝██║░░██║███████╗░░░██║░░░
        # ╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝░░░░░░░░░░░░░░░░░░░░░╚═════╝░╚═╝░░╚═╝╚══════╝░░░╚═╝░░░

        hashed = bcrypt.hashpw(password, account['salt'].encode()).decode()

        if hashed == account['password_hash']:
            # we're good to login!
            response = http_301('/')

            auth_token: str = secrets.token_urlsafe(30)
            cookie = Cookie(
                name='auth_token',
                value=auth_token,
                max_age=7200,
                secure=False,
                http_only=True
            )
            response.add_cookie(cookie)
            auth_token_salt = b'$2b$12$Fr9yR03IQLCGqjB1MJ9gfu'
            auth_token_hash = bcrypt.hashpw(auth_token.encode(), auth_token_salt)
            add_token(username, auth_token_hash.decode())

            print('successful login')
            return socket.request.sendall(response.write_raw())
            
        else:
            print('failed login attempt')
            arguments = {'username_exists': True, 'correct_password': False}
            response: Response = http_200('text/html', FileIO('html/login.html').read(arguments), 'utf-8')
            return socket.request.sendall(response.write_raw())

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

def register(socket, request: Request):
    if request.request_type == 'GET':
        response = http_200('text/html', FileIO('html/register_response.html').read({'static': True}), 'utf-8')
        socket.request.sendall(response.write_raw())

    elif request.request_type == 'POST':
        form: Dict[str, bytes] = parse_form(request)
        email = form['email'].decode()
        username = form['username'].decode()
        password = form['password']
        print(password)

        if not check_password(str(password)):
            arguments = {'static': False, 'username_taken': False, 'good_password': False}
            response = http_200('text/html', FileIO('html/register_response.html').read(arguments), 'utf-8')
            return socket.request.sendall(response.write_raw())

        # ██╗░░██╗░█████╗░░██████╗██╗░░██╗░░░░░░░░░░░░░░░░░░░░░░██████╗░█████╗░██╗░░░░░████████╗
        # ██║░░██║██╔══██╗██╔════╝██║░░██║░░░░░░░░░██╗░░░░░░░░░██╔════╝██╔══██╗██║░░░░░╚══██╔══╝
        # ███████║███████║╚█████╗░███████║░░░░░░░██████╗░░░░░░░╚█████╗░███████║██║░░░░░░░░██║░░░
        # ██╔══██║██╔══██║░╚═══██╗██╔══██║░░░░░░░╚═██╔═╝░░░░░░░░╚═══██╗██╔══██║██║░░░░░░░░██║░░░
        # ██║░░██║██║░░██║██████╔╝██║░░██║░░░░░░░░░╚═╝░░░░░░░░░██████╔╝██║░░██║███████╗░░░██║░░░
        # ╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝░░░░░░░░░░░░░░░░░░░░░╚═════╝░╚═╝░░╚═╝╚══════╝░░░╚═╝░░░

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt).decode()

        account = create_account(str(email), username, hashed, salt.decode())

        if account:
            arguments = {'static': False, 'username_taken': False, 'good_password': True, 'registered': True}
            response = http_200('text/html', FileIO('html/register_response.html').read(arguments), 'utf-8')
            return socket.request.sendall(response.write_raw())
        else:
            arguments = {'static': False, 'username_taken': True, 'good_password': True}
            response = http_200('text/html', FileIO('html/register_response.html').read(arguments), 'utf-8')
            return socket.request.sendall(response.write_raw())

    else:
        raise InvalidRequest


def auth(socket, request: Request) -> bytes:
    if request.request_type == 'GET':
        if request.cookies and 'auth_token' in request.cookies:
            salt = b'$2b$12$Fr9yR03IQLCGqjB1MJ9gfu'
            auth_token_hash: str = bcrypt.hashpw(request.cookies['auth_token'].encode(), salt).decode()
            account = get_account_from_token(auth_token_hash)

            if account and account['auth_token_hash'] == auth_token_hash:
                username = account['username']
                arguments = {'username': username}
                response = http_200('text/html', FileIO('html/big_yoshi_account.html').read(arguments), 'utf-8')
                return socket.request.sendall(response.write_raw())

        response = http_403('text/html', 'Please log in to view this content'.encode())
        return socket.request.sendall(response.write_raw())

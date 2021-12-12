import re
import string
from typing import Dict
import bcrypt
import secrets
import sys
from crablib.misc import print

from crablib.fileIO import FileIO
from crablib.http.parse import Request, parse_form, Response, Cookie
from crablib.http.response import http_200, InvalidRequest, http_301, http_403
from crablib.auth import get_request_account
from db.account import create_account, get_account, add_token, \
    get_account_from_token, login as dblogin, logout as dblogout



def login(socket, request: Request):
    if request.request_type == 'GET':
        response: Response = http_200('text/html', FileIO('html/login.html').read_template(), 'utf-8')
        return socket.request.sendall(response.write_raw())

    elif request.request_type == 'POST':
        form: Dict[str, bytes] = parse_form(request)
        print(f'form: {form}')
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

            dblogin(username)

            print('successful login')
            return socket.request.sendall(response.write_raw())

        else:
            print('failed login attempt')
            arguments = {'username_exists': True, 'correct_password': False}
            response: Response = http_200('text/html', FileIO('html/login.html').read(arguments), 'utf-8')
            return socket.request.sendall(response.write_raw())

    else:
        raise InvalidRequest


def logout(socket, request: Request):
    account = get_request_account(request)
    if request.request_type == 'GET' and account:
        response = http_200('text/html', FileIO('html/logged_out.html').read())
        logout_cookie = Cookie(
            name='auth_token',
            value="logged-out",
            max_age=0,
            secure=False,
            http_only=True
        )
        response.add_cookie(logout_cookie)
        dblogout(account['username'])
        return socket.request.sendall(response.write_raw())

    raise InvalidRequest


def check_password(password: str) -> bool:
    conditions = [
        len(password) >= 8,
        len(re.findall('[a-z]', password)) >= 1,
        len(re.findall('[A-Z]', password)) >= 1,
        len(re.findall('[0-9]', password)) >= 1,
        len(re.findall(f'[{string.punctuation}]', password))
    ]
    for condition in conditions:
        if not condition:
            return False
    return True


def register(socket, request: Request):
    if request.request_type == 'GET':
        response = http_200('text/html', FileIO('html/register.html').read({'static': True}), 'utf-8')
        socket.request.sendall(response.write_raw())

    elif request.request_type == 'POST':
        form: Dict[str, bytes] = parse_form(request)
        email = form['email'].decode()
        username = form['username'].decode()
        password = form['password']
        misc.print(password)

        if not check_password(str(password)):
            arguments = {'static': False, 'username_taken': False, 'good_password': False}
            response = http_200('text/html', FileIO('html/register.html').read(arguments), 'utf-8')
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
            response = http_200('text/html', FileIO('html/register.html').read(arguments), 'utf-8')
            return socket.request.sendall(response.write_raw())
        else:
            arguments = {'static': False, 'username_taken': True, 'good_password': True}
            response = http_200('text/html', FileIO('html/register.html').read(arguments), 'utf-8')
            return socket.request.sendall(response.write_raw())

    else:
        raise InvalidRequest

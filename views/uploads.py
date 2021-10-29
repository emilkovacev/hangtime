import re
import os
import secrets
from typing import List, Dict

from crablib.http.response import http_200, http_301, http_403, http_404
from crablib.http.parse import Request, escape, parse_form, Response
from crablib.fileIO import FileIO


message_list: List[str] = []
image_list: List[str] = []
xsrf: Dict[str, str] = {}

def index(request: Request) -> bytes:
    return http_200(
        content_type='text/html',
        content=FileIO('html/index.html').read(),
        charset='utf-8'
    ).write_raw()

def uploads(request: Request) -> bytes:
    global xsrf
    xsrf['text'], xsrf['image'] = secrets.token_urlsafe(32), secrets.token_urlsafe(32)

    return http_200(
        content_type='text/html',
        content=FileIO('html/uploads.html').read(
            {
                'messages': message_list,
                'images': image_list,
                'xsrf_image': xsrf['image'],
                'xsrf_text': xsrf['text']
            }),
        charset='utf-8'
    ).write_raw()


def yoshi(request: Request) -> bytes:
    return http_200(
        content_type='text/html',
        content=FileIO('html/yoshi.html').read(),
        charset='utf-8'
    ).write_raw()


def images(request: Request) -> bytes:
    retval = {}
    arguments = re.compile("(?<=\\?).+")
    search = arguments.search(request.path)

    for arg in search.group(0).split('&'):
        arg = arg.split('=')
        if arg[1].count('+') > 0:
            if arg[0] == 'images':
                retval[arg[0]] = [f'images/{x}.jpg' for x in arg[1].split('+')]
            else:
                retval[arg[0]] = [x for x in arg[1].split('+')]
        else:
            if arg[0] == 'images':
                retval[arg[0]] = f'images/{arg[1]}.jpg'
            else:
                retval[arg[0]] = arg[1]

    return http_200(
        content_type='text/html',
        content=FileIO('html/images.html').read(retval)
    ).write_raw()


# text/css
def css(request: Request) -> bytes:
    return http_200(
        content_type='text/css',
        content=FileIO('style/style.css').read(),
        charset='utf-8'
    ).write_raw()


# script/js
def js(request: Request) -> bytes:
    return http_200(
        content_type='text/javascript',
        content=FileIO('script/script.js').read()
    ).write_raw()


# image/jpg
def img(request: Request) -> bytes:
    return http_200(
        content_type='image/jpeg',
        content=FileIO(request.path.lstrip('/')).read()
    ).write_raw()


# forms
def form_upload(request: Request) -> bytes:
    form: Dict[str, bytes] = parse_form(request)
    if 'xsrf' not in form or form['xsrf'].decode() != xsrf['text']:
        return http_403(
            content_type='text/html',
            content=FileIO('html/403.html').read()
        ).write_raw()

    author = escape(form["name"].decode())
    message = escape(form["yoshi"].decode())
    message_list.append(f'<p><b>{author}</b>: {message}</p>')

    return http_301('/').write_raw()


def generate_filename():
    secret = ''
    while not secret or f'{secret}.jpg' in os.listdir('../images'):
        secret = secrets.token_urlsafe(10)
    return secret


def image_upload(request: Request) -> bytes:
    form: Dict[str, bytes] = parse_form(request)

    if 'xsrf' not in form or form['xsrf'].decode() != xsrf['image']:
        return http_403(
            content_type='text/html',
            content=FileIO('html/403.html').read()
        ).write_raw()

    if 'name' in form and '/' not in form['name'].decode() and f'images/{form["name"].decode()}.jpg' not in image_list:
        filename: str = escape(generate_filename())
        caption = escape(form["name"].decode())
        url = f'images/{filename}.jpg'
        with open(url, 'wb') as f:
            f.write(form['upload'])
        image_list.append(f'<div class="upload"><img src="{escape(url)}" />'
                          f'<figcaption><i>{caption}</i></figcaption></div>')
    return http_301('/').write_raw()

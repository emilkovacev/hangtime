from .parse import ParseTools as pt
from crablib.htmlgen.generate import generate_html


def http_200(content_type: str, content: bytes, charset: str = None) -> bytes:
    headers = {
      'Content-Type': content_type,
      'Content-Length': len(content.strip()),
      'X-Content-Type-Options': 'nosniff',
    }

    if charset:
        headers['Content-Type'] += f'; charset={charset}'

    response = pt.write_raw(
        status_code=200,
        status_message='OK',
        headers=headers,
        body=content,
    )

    return response


def http_301(path: str) -> bytes:
    print(path)
    response = pt.write_raw(
        status_code=301,
        status_message='Moved Permanently',
        headers={
            'Location': path,
            'Content-Length': 0,
        },
    )
    return response


def http_404(content_type: str, content: bytes) -> bytes:
    response = pt.write_raw(
        status_code=404,
        status_message='Not Found',
        headers={
            'Content-Type': content_type,
            'Content-Length': len(content.strip()),
        },
        body=content,
    )
    return response


def text(txt_input: str):
    return txt_input.encode()


def read(path: str) -> bytes:
    with open(path, 'r', errors='strict', buffering=1) as f:
        return f.read().encode()


def html(path: str, arguments=None) -> bytes:
    with open(path, 'r', errors='strict', buffering=1) as f:
        return generate_html(f.read(), arguments).encode()


def image(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()
from .parse import ParseTools as pt

utf_options = {
    'text/plain': '',
    'text/html': 'charset=utf8',
    'text/css': '',
    'text/javascript': '',
    'image/png': '',
    'image/jpeg': '',
    'video/mp4': ''
}


def http_200(content_type: str, content: bytes) -> bytes:
    status_code: int = 200
    status_message: str = 'OK'
    headers = {
        'Content-Type': f'{content_type}; {utf_options[content_type]}',
        'Content-Length': str(len(content)),
        'X-Content-Type-Options': 'nosniff',
    }
    body = content

    return pt.write_raw(status_code=status_code, status_message=status_message, headers=headers, body=body)


def http_301(path: str) -> bytes:
    response = pt.write_response(
        status_code=301,
        status_message='Moved Permanently',
        headers={
            'Location': path,
        },
    )
    return response.encode()


def http_404(content_type: str, content: bytes) -> bytes:
    response = pt.write_raw(
        status_code=404,
        status_message='Not Found',
        headers={
            'Content-Type': content_type,
            'Content-Length': str(len(content)),
        },
        body=content,
    )
    return response


def text(txt_input: str):
    return txt_input.encode()


def read(path: str) -> bytes:
    with open(path, 'r', errors='strict', buffering=1) as f:
        return f.read().encode()


def image(path: str) -> bytes:
    return read(path)

from crablib.http.parse import Response


def http_200(content_type: str, content: bytes, charset: str = None) -> Response:
    headers = {
      'Content-Type': content_type,
      'Content-Length': len(content.strip()),
      'X-Content-Type-Options': 'nosniff',
    }

    if charset:
        headers['Content-Type'] += f'; charset={charset}'

    response = Response(
        status_code=200,
        status_message='OK',
        headers=headers,
        body=content,
    )

    return response


def http_301(path: str) -> Response:
    response = Response(
        status_code=301,
        status_message='Moved Permanently',
        headers={
            'Location': path,
            'Content-Length': 0,
        },
    )
    return response


def http_403(content_type: str, content: bytes) -> Response:
    response = Response(
        status_code=403,
        status_message='Forbidden Response',
        headers={
            'Content-Type': content_type,
            'Content-Length': len(content.strip()),
        },
    )
    return response


def http_404(content_type: str, content: bytes) -> Response:
    response = Response(
        status_code=404,
        status_message='Not Found',
        headers={
            'Content-Type': content_type,
            'Content-Length': len(content.strip()),
        },
        body=content,
    )
    return response

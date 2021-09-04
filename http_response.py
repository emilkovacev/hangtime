from http_parse import ParseTools as pt


def http_200(content_type: str, content: str) -> str:
    response = pt.write_response(
        status_code=200,
        status_message='OK',
        headers={
            'Content-Type': content_type,
            'Content-Length': str(len(content)),
        },
        body=content,
    )
    return response


def http_301(path: str) -> str:
    response = pt.write_response(
        status_code=301,
        status_message='Moved Permanently',
        headers={
            'Location': path,
        },
    )
    return response


def http_404(content_type: str, content: str):
    response = pt.write_response(
        status_code=404,
        status_message='Not Found',
        headers={
            'Content-Type': content_type,
            'Content-Length': str(len(content)),
        },
        body=content,
    )
    return response

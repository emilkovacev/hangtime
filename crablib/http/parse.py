import re
from crablib.htmlgen.newgen import generate_html
from crablib.querygen.reader import read_query


class Request:
    def __init__(self, request, request_type, path, http_version, headers, body=None):
        self.request = request
        self.request_type: str = request_type
        self.path: str = path
        self.http_version: str = http_version
        self.headers: {str: str} = headers
        self.body = body

    def __str__(self):
        return [self.http_version, self.path, self.request_type]


def parse_request(request: str) -> Request:
    content: [str] = request.split('\r\n\r\n')  # separation of request/headers and body
    lines = content[0].split('\r\n')  # lines of request/headers
    request_line = lines[0].split(' ')
    headers = lines[1:]

    request_type = request_line[0]
    path = request_line[1]
    http_version = request_line[2]  # safely assume is HTTP/1.1
    body = None
    if len(content) == 2: body = content[1]

    ret_headers = {}
    for header in headers:
        pair: [str] = re.split(':\\s*', header)
        ret_headers[pair[0]] = pair[1]

    return Request(
        request=request,
        request_type=request_type,
        path=path,
        http_version=http_version,
        body=body,
        headers=ret_headers
    )


class Response:
    def __init__(self, status_code: int, status_message: str, headers,
                 body: bytes = None, http_version: str = 'HTTP/1.1'):
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers
        self.body = body
        self.http_version = http_version

    def write_raw(self) -> bytes:
        response: bytes = f'{self.http_version} {self.status_code} {self.status_message}\r\n'.encode()
        for (key, value) in self.headers.items():
            response += f'{key}: {str(value)}\r\n'.encode()

        if self.body:
            response += '\r\n'.encode()
            response += self.body

        return response.rstrip('\r\n'.encode())

    def __str__(self):
        return [self.http_version, self.status_code, self.status_message]


class FileIO:
    def __init__(self, path, query=None):
        self.path = path
        self.query = query
        self.extension = self.find_extension()

    def find_extension(self) -> str:
        match = re.search('(?<=\\.)[^.]+$', self.path)
        if match:
            return match.group(0)
        else:
            return ''

    def read(self) -> bytes:
        ext = self.extension
        if ext == 'html' and self.query and self.query.isvalid():
            with open(self.path, 'r') as f:
                return generate_html(f.read(), self.query).encode()

        else:
            with open(self.path, 'rb') as f:
                return f.read()

import re
from typing import Dict, List, Tuple


class Request:
    def __init__(self, request: bytes, request_type: str,
                 path: str, headers: Dict[str, str], http_version: str = 'HTTP/1.1', body: bytes = b''):
        self.request = request
        self.request_type = request_type
        self.path = path
        self.http_version = http_version
        self.headers = headers
        self.body = body

    def __str__(self):
        return [self.http_version, self.path, self.request_type]


def parse_request(request: bytes) -> Request:
    i = re.match(b'^.+?(?=\r\n\r\n)', request, re.DOTALL).end()
    header: str = request[:i].decode()
    lines = header.split('\r\n')

    first_line = lines[0].split(' ')
    request_type, path = first_line[0], first_line[1]
    headers = lines[1:]

    parsed_headers = {}
    for h in headers:
        parts = re.split(':\\s*', h)
        parsed_headers[parts[0]] = parts[1]

    body: bytes = b''
    if 'Content-Length' in parsed_headers:
        body = request[i + 4: i + 4 + int(parsed_headers['Content-Length'])]

    return Request(
        request=request,
        request_type=request_type,
        path=path,
        headers=parsed_headers,
        body=body
    )

class Header:
    def __init__(self, name: str, value: str, options: Dict[str, str]):
        self.name: str = name
        self.value: str = value
        self.options: Dict[str, str] = options

def parse_header(s: str) -> Header:
    values = re.split('[;:]\\s*', s)
    name: str = values[0]
    value: str = values[1]

    options = {}
    if len(values) >= 3:
        for option in values[2:]:
            desc = re.match('(?P<opt>.+)="(?P<value>.*)"', option)
            opt, opt_value = desc.groupdict()['opt'], desc.groupdict()['value']
            options[opt] = opt_value

    return Header(name=name, value=value, options=options)


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


def escape(html: str) -> str:
    return html \
        .replace('<', '&#60;') \
        .replace('>', '&#62;') \
        .replace('=', '&#61')


def parse_form(request: Request) -> Dict[str, bytes]:
    boundary: str = '--' + re.search('boundary=(?P<boundary>.+);?', request.headers['Content-Type']).group(1)
    content_chunks: List[bytes] = request.body.split(boundary.encode())[1:-1]

    retval: Dict[str, bytes] = {}
    content: bytes
    for content in content_chunks:
        parsed_content: List[bytes] = content.strip(b'\r\n').split(b'\r\n\r\n')
        headers: List[str] = parsed_content[0].decode().split('\r\n')
        body: bytes = b''
        if len(parsed_content) == 2:
            body = parsed_content[1]

        headers_dict: Dict[str, Header] = {}
        header: str
        for header in headers:
            headerobj: Header = parse_header(header)
            headers_dict[headerobj.name] = headerobj
            content_name: str = headers_dict['Content-Disposition'].options['name']
            retval[content_name] = body
    return retval

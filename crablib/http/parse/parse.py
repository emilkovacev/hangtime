import re


class Header:
    def __init__(self, value: str, options: {str: str}):
        self.value = value
        self.options = options


class Request:
    def __init__(self, request: bytes, request_type: str,
                 path: str, http_version: str, headers: {str: Header}, body: bytes = None):
        self.request = request
        self.request_type = request_type
        self.path = path
        self.http_version = http_version
        self.headers = headers
        self.body = body

    def __str__(self):
        return [self.http_version, self.path, self.request_type]


def parse_form(request: Request) -> {str: str}:
    boundary = re.search('boundary=(?P<boundary>.+);*', request.headers['Content-Type']).groupdict()['boundary']
    content = re.split(b'--' + boundary.encode(), request.body)
    print(content)


def parse_header(s: str) -> Header:
    values = re.split('[;:]\\s*', s)
    name, value = values[0], values[1]

    options = {}
    if len(values) >= 3:
        for option in values[2:]:
            desc = re.match('(?P<opt>.+)="(?P<value>.+)"', option)
            opt, opt_value = desc.groupdict()['opt'], desc.groupdict()['value']
            options[opt] = opt_value

    return Header(value=value, options=options)


def parse_request(request: bytes) -> Request:
    i = 0
    while request[i:i + 4] != b'\r\n\r\n' and i < len(request):
        i += 1

    content: [str] = request[:i].decode()
    lines = content.split('\r\n')  # lines of request/headers
    request_line = lines[0].split(' ')
    headers = lines[1:]

    request_type = request_line[0]
    path = request_line[1]
    http_version = request_line[2]  # safely assume is HTTP/1.1

    ret_headers: {str: Header} = {}
    for header in headers:
        title: str = re.match('.+(?=:\\s*)', header).group(0)
        ret_headers[title] = parse_header(header)

    body = None
    if 'Content-Length' in ret_headers:
        header: Header = ret_headers['Content-Length']
        body = request[i + 4: i + 4 + int(header.value)]

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

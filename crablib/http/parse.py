import re
from typing import Dict, List


class Request:
    def __init__(self, request: bytes, request_type: str,
                 path: str, headers: Dict[str, str], http_version: str = 'HTTP/1.1',
                 cookies: Dict[str, str] = None, body: bytes = b''):
        self.request = request
        self.request_type = request_type
        self.path = path
        self.http_version = http_version
        self.headers = headers
        self.body = body
        self.cookies: Dict[str, str] = cookies

    def __str__(self):
        return [self.http_version, self.path, self.request_type]


def parse_request(request: bytes) -> Request:
    i = re.match(b'^.+?(?=\r\n\r\n)', request, re.DOTALL).end()
    header: str = request[:i].decode()
    lines = header.split('\r\n')

    first_line = lines[0].split(' ')
    request_type, path = first_line[0], first_line[1]
    headers = lines[1:]

    parsed_headers: Dict[str, str] = {}
    for h in headers:
        parts = re.split(':\\s*', h)
        parsed_headers[parts[0]] = parts[1]

    body: bytes = b''
    if 'Content-Length' in parsed_headers:
        body = request[i + 4: i + 4 + int(parsed_headers['Content-Length'])]

    cookies = {}
    if 'Cookie' in parsed_headers:
        parts = re.split('; ', parsed_headers['Cookie'])
        for cookie in parts:
            sections = cookie.split('=')
            cookies[sections[0]] = sections[1]

    return Request(
        request=request,
        request_type=request_type,
        path=path,
        headers=parsed_headers,
        body=body,
        cookies=cookies
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


class Cookie:
    def __init__(self, name: str, value: str, expires: str = None,
                 max_age: int = None, secure: bool = True, http_only: bool = True,
                 same_site: str = 'Strict', path: str = None):
        self.name: str = name
        self.value: str = value
        self.expires = expires
        self.max_age = str(max_age)
        self.secure = secure
        self.http_only = http_only
        self.path = path
        self.same_site = same_site

    def write(self) -> str:
        response: str = f'{self.name}={self.value}'
        if self.expires:
            response += f'; Expires={self.expires}'
        if self.max_age:
            response += f'; Max-Age={self.max_age}'
        if self.secure:
            response += f'; Secure'
        if self.http_only:
            response += f'; HttpOnly'
        if self.path:
            response += f'; Path={self.path}'
        if self.same_site:
            response += f'; SameSite={self.same_site}'
        return response

    def __str__(self) -> str:
        return self.write()


class Response:
    def __init__(self, status_code: int, status_message: str, headers,
                 body: bytes = None, http_version: str = 'HTTP/1.1'):
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers
        self.body = body
        self.http_version = http_version
        self.cookies: Dict[str, Cookie] = {}

    def write_raw(self) -> bytes:
        response: bytes = f'{self.http_version} {self.status_code} {self.status_message}\r\n'.encode()
        for (key, value) in self.headers.items():
            response += f'{key}: {str(value)}\r\n'.encode()

        for cookie in self.cookies.values():
            response += f'Set-Cookie: {cookie.write()}\r\n'.encode()

        response += b'\r\n'

        if self.body:
            response += self.body

        return response

    def add_cookie(self, cookie: Cookie):
        self.cookies[cookie.name] = cookie

    def __str__(self):
        return [self.http_version, self.status_code, self.status_message]


def parse_cookie(cookie: str) -> Dict[str, Cookie]:
    cookie_list = re.split(': ', cookie)
    retval: Dict[str, Cookie] = {}
    for c in cookie_list:
        c_headers = c.split('=')
        retval[c_headers[0]] = Cookie(
            name=c_headers[0],
            value=c_headers[1]
        )
    return retval


def escape(html: str) -> str:
    return html \
        .replace('<', '&lt;') \
        .replace('>', '&gt;') \
        .replace('&', '&amp;')


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


def unmask(chunk: bytes, masking_key: bytes) -> bytes:
    i = 0
    retval = b''
    for b in chunk:
        if i > 3: i = 0
        retval += (b ^ masking_key[i]).to_bytes(1, 'little')
        i += 1
    return retval


def bytes_to_int(byt: bytes) -> int:
    retval = 0
    for i in range(len(byt)):
        pw = 2 * (len(byt) - i - 1)
        retval += byt[i] * (16 ** pw)
    return retval


class Frame:
    def __init__(self, FIN: int, RSV1: int, RSV2: int, RSV3: int,
                 opcode: int, MASK, payload_len: int, data: bytes,
                 masking_key: bytes = None):
        self.FIN = FIN
        self.RSV1 = RSV1
        self.RSV2 = RSV2
        self.RSV3 = RSV3

        self.opcode = opcode
        self.MASK = MASK
        self.payload_len = payload_len
        self.masking_key = masking_key

        self.data: bytes = data

    def escape(self):
        self.data = self.data \
            .replace(b'&', b'&amp;') \
            .replace(b'<', b'&lt;') \
            .replace(b'>', b'&gt;')

        self.payload_len = len(self.data)

    def write_raw(self):
        self.escape()
        retval = b'\x81'
        if self.payload_len < 126:
            retval += self.payload_len.to_bytes(1, 'big')

        else:
            retval += b'\x7e'
            retval += self.payload_len.to_bytes(2, 'big')

        retval += self.data
        return retval

    def __str__(self):
        raw = self.write_raw()
        output = ''
        i = 1
        for b in raw:
            output += (format(b, '08b')) + ' '
            if i % 4 == 0: output += '\n'
            i += 1
        return output


def parse_frame(frame: bytes) -> Frame:
    PAYLOAD_SB = 2
    MASK_SB = 2
    payload_len: int = frame[1] & 0x7f

    if payload_len == 126:
        payload_len = bytes_to_int(frame[2:4])
        PAYLOAD_SB = MASK_SB = 4

    payload: bytes = b''
    masking_key = None
    MASK = (frame[1] & 0x80) >> 7
    if MASK:
        PAYLOAD_SB += 4
        masking_key = bytes(x for x in frame[MASK_SB:MASK_SB + 4])
        payload += unmask(frame[PAYLOAD_SB:], masking_key)

    else:
        payload = frame[PAYLOAD_SB:]

    parsed_frame = Frame(
        FIN=(frame[0] & 0x80) >> 7,
        RSV1=(frame[0] & 0x40) >> 6,
        RSV2=(frame[0] & 0x20) >> 5,
        RSV3=(frame[0] & 0x10) >> 4,

        MASK=MASK,
        opcode=frame[0] & 0x0f,

        payload_len=payload_len,
        masking_key=masking_key,
        data=payload
    )
    return parsed_frame

class ParseTools:
    """
    Parse HTTP str input
    Write HTTP str output
    """

    @classmethod
    def parse_request(cls, request: str) -> {str: str}:
        parsed = {}  # dict with parsed values of request

        content: [str] = request.split('\r\n\r\n')  # separation of request/headers and body
        lines = content[0].split('\r\n')  # lines of request/headers
        request_line = lines[0].split(' ')
        headers = lines[1:]

        parsed['request_type'] = request_line[0]
        parsed['path'] = request_line[1]
        parsed['http_version'] = request_line[2]  # safely assume is HTTP/1.1
        if len(content) == 2: parsed['body'] = content[1]

        for header in headers:
            pair = header.split(': ')
            parsed[pair[0]] = pair[1]

        return parsed

    @classmethod
    def write_response(cls, status_code: int, status_message: str, headers, body: str = '',
                       http_version: str = 'HTTP/1.1') -> str:
        # check for spaces in http_version and status_code
        response = f'{http_version} {status_code} {status_message}\r\n'
        for (key, value) in headers.items():
            response += f'{key}: {str(value)}\r\n'

        if body:
            response += '\r\n'
            response += body

        return response.rstrip('\r\n')

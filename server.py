import re
import socketserver

from crablib.http.parse import Request, parse_request, FileIO
from crablib.http.response import http_404

from urls import urls, Path


class CrabServer(socketserver.BaseRequestHandler):
    def send_response(self, response: bytes):
        self.request.sendall(response)
        return

    def handle(self):
        request: Request = parse_request(self.request.recv(1024))

        response_404 = http_404(
            content_type='text/html',
            content=FileIO('crablib/error_templates/404.html').read()
        )

        item: Path
        for item in urls:
            match = re.match(item.regex, request.path)

            if match:
                try:
                    self.send_response(item.view(request))
                except FileNotFoundError:
                    self.send_response(response_404.write_raw())

        self.send_response(response_404.write_raw())
        return

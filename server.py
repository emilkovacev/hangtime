import random
import re
import socketserver

from crablib.fileIO import FileIO
from crablib.http.parse import Request, parse_request
from crablib.http.response import http_404

from urls import urls, Path


class CrabServer(socketserver.BaseRequestHandler):
    def send_response(self, response: bytes):
        self.request.sendall(response)
        return

    def handle(self):
        raw: bytes = self.request.recv(2048)
        request: Request = parse_request(raw)
        if 'Content-Type' in request.headers and request.headers['Content-Type'].split(';')[0] == 'multipart/form-data':
            content_length: int = len(request.body)
            length = int(request.headers.get('Content-Length', 0))  # if content-length, add length

            while content_length < length:
                req = self.request.recv(1024)
                content_length += len(req)
                request.body += req

        response_404 = http_404(
            content_type='text/html',
            content=FileIO('html/404.html').read()
        )

        item: Path
        for item in urls:
            match = re.match(item.regex, request.path)

            if match:
                try:
                    self.send_response(item.view(request))
                    return
                except Exception as e:
                    self.send_response(response_404.write_raw())
                    print(e)
        self.send_response(response_404.write_raw())
        return


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', random.randint(2000, 9000)
    print(f'starting server for {HOST} at {PORT}')
    with socketserver.ThreadingTCPServer((HOST, PORT), CrabServer) as server:
        server.serve_forever()

import random
import re
import socketserver
from random import randint
import traceback
import webbrowser

from crablib.fileIO import FileIO
from crablib.http.parse import Request, parse_request
from crablib.http.path import Path
from crablib.http.response import http_404
from urls import urls


class CrabServer(socketserver.BaseRequestHandler):
    clients = []
    chatclients = {}

    def handle(self):
        raw: bytes = self.request.recv(2048)
        if len(raw) == 0: return
        request: Request = parse_request(raw)

        self.match(request)

    def match(self, request):
        response_404 = http_404('text/html', FileIO('html/404.html').read())

        item: Path
        for item in urls:
            match = re.match(item.regex, request.path)
            if match:
                try:
                    item.view(self, request)
                    return
                except Exception as e:
                    self.request.sendall(response_404.write_raw())
                    print(e)
                    print(traceback.format_exc())
                    print('----------------------')
        self.request.sendall(response_404.write_raw())


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 8000
    print(f'starting server for {HOST} at {PORT}')
    with socketserver.ThreadingTCPServer((HOST, PORT), CrabServer) as server:
        webbrowser.open(f'http://localhost:{PORT}')
        server.serve_forever()

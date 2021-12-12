import random
import re
import socketserver
from random import randint
import traceback
import webbrowser
import argparse

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

        item: Path
        for item in urls:
            match = re.match(item.regex, request.path)
            if match:
                try:
                    item.view(self, request)
                    return
                except Exception as e:
                    arguments = {'exception': str(e), 'traceback': traceback.format_exc()}
                    response_404 = http_404('text/html', FileIO('html/error.html').read(arguments))
                    self.request.sendall(response_404.write_raw())
        response_404 = http_404('text/html', FileIO('html/error.html').read())
        self.request.sendall(response_404.write_raw())


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', randint(1000, 9999)
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", type=str, help="bind host and port")
    args = parser.parse_args()
    if args.bind:
        HOST, PORT = args.bind.split(':')

    print(f'starting server for {HOST} at {PORT}')
    with socketserver.ThreadingTCPServer((HOST, int(PORT)), CrabServer) as server:
        webbrowser.open(f'http://localhost:{PORT}')
        server.serve_forever()

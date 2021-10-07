import socketserver
import sys

from crablib.http.response import *
from crablib.querygen.reader import *


class CrabServer(socketserver.BaseRequestHandler):
    def send_response(self, response):
        self.request.sendall(response)

    def route(self, func, regex):
        if re.match(regex, self.request.recv(1024)):
            self.request.sendall(func())

    def handle(self):
        received_data = self.request.recv(1024)  # receive data
        if len(received_data) == 0:
            return

        parsed: {str: str} = pt.parse_request(received_data.decode())  # parse decoded input into dict
        path = parsed['path']

        print(path)

        if re.match('^/$', path):
            file = http_200('text/html', read('html/index.html'), 'utf-8')
            self.send_response(file)

        elif re.match('^/images/[^.]+\\.\\w+$', path):
            pass

        elif re.match('^/images/(?P<title>[^. ]+)\\.(?P<file>(png|jpg|jpeg))+$', path):
            filename = re.match("[^/]+.$", path)
            file_ext = re.match("(?<=[.]).+$", path)

            try:
                file = http_200(f'image/{file_ext.string}', image(f'image/{filename}'))
                self.send_response(file)
            except FileNotFoundError:
                file = http_404('text/html', read('crablib/error_templates/404.html'))
                self.send_response(file)
        elif re.match('^/images?.+', path):
            arguments = read_query(path)
            try:
                file = http_200(f'text/html', html('html/index.html', arguments))
                self.send_response(file)
            except FileNotFoundError:
                file = http_404('text/html', read('crablib/error_templates/404.html'))
                self.send_response(file)

        elif re.match('^/style/style.css$', path):
            file = http_200('text/css', read('style/style.css'), 'utf-8')
            self.send_response(file)

        elif re.match('^/js.script.js$', path):
            file = http_200('text/javascript', read('js/script.js'), 'utf-8')
            self.send_response(file)

        elif re.match('^/utf.txt$', path):
            file = http_200('text/html', read('utf.txt'), 'utf-8')
            self.send_response(file)

        elif re.match('^/hello$', path):
            response = http_200('text/plain', text('Hello world!'))
            self.send_response(response)

        elif re.match('^/hi$', path):
            response = http_301('/hello')
            self.send_response(response)

        else:
            file = http_404('text/html', read('crablib/error_templates/404.html'))
            self.send_response(file)


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', int(sys.argv[1])
    print(f'starting server for {HOST} at {PORT}')
    with socketserver.ThreadingTCPServer((HOST, PORT), CrabServer) as server:
        server.serve_forever()

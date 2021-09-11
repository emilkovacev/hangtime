import socketserver
from httplib.response import *  # I made my own http library :)


class MyTCPHandler(socketserver.BaseRequestHandler):
    def send_response(self, response):
        self.request.sendall(response)

    def handle(self):
        received_data = self.request.recv(1024).strip()  # receive data
        if len(received_data) == 0:
            return

        parsed: {str: str} = pt.parse_request(received_data.decode())  # parse decoded input into dict
        path = parsed['path']

        print(path)

        if path == '/':
            file = http_200('text/html', read('index.html'), 'utf-8')
            self.send_response(file)

        elif path[0:6] == '/image':
            file = http_200('img/jpeg', image(f'image/{path[7:]}'))
            self.send_response(file)

        elif path == '/style/style.css':
            file = http_200('text/css', read('style/style.css'), 'utf-8')
            self.send_response(file)

        elif path == '/js/script.js':
            file = http_200('text/javascript', read('js/script.js'), 'utf-8')
            self.send_response(file)

        elif path == '/utf.txt':
            file = http_200('text/html', read('utf.txt'), 'utf-8')
            self.send_response(file)

        elif path == '/hello':
            response = http_200('text/plain', text('Hello world!'))
            self.send_response(response)

        elif path == '/hi':
            response = http_301('/hello')
            self.send_response(response)

        else:
            response = http_404('text/plain', text('The requested content does not exist, Jesse >:('))
            self.send_response(response)


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 8000
    print('starting server...')
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
        server.allow_reuse_address = True  # python socketserver documentation (allows address reuse when running)

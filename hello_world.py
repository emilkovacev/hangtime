import socketserver
from http_response import *  # a library I wrote while working on this project

class MyTCPHandler(socketserver.BaseRequestHandler):
    def send_response(self, response):
        self.request.sendall(response.encode())

    def handle(self):
        recieved_data = self.request.recv(1024).strip()                 # recieve data
        parsed: {str: str} = pt.parse_request(recieved_data.decode())   # parse decoded input into dict

        path = parsed['path']
        if path == '/hi':
            response = http_301('/hello')
            self.send_response(response)

        elif path == '/hello':
            response = http_200('text/plain', 'Hello world!')
            self.send_response(response)

        else:
            response = http_404('text/plain', 'The requested content does not exist')
            self.send_response(response)


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 8000
    print('starting server...')
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()


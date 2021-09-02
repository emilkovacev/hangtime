import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        recieved_data = self.request.recv(1024).strip()
        print(self.client_address[0] + ' is sending data:')
        print(recieved_data.decode())
        print('\n\n')
        response =  'HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello world!'.encode()
        self.request.sendall(response)


if __name__ == '__main__':
    HOST, PORT = 'localhost', 8000

    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()


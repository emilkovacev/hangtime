import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    @classmethod
    def find_path(self, request):
        return request.split(' ')[1]

    def handle(self):
        recieved_data = self.request.recv(1024).strip() # recieve data
        path = self.find_path(recieved_data.decode())   # find host from decoded str

        if path == '/hello':
            response =  """HTTP/1.1 200 OK\r\n
                        Content-Length: 12\r\n\r\n
                        Hello world!""".encode()        # encode response body
            self.request.sendall(response)              # send response

        else:
            response =  """HTTP/1.1 404 Not Found\r\n
                        Content-Type: text/plain\r\n
                        content-length: 36\r\n\r\n
                        The requested content does not exist""".encode()

            self.request.sendall(response)


if __name__ == '__main__':
    HOST, PORT = 'localhost', 8000

    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()


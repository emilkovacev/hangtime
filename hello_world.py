import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    @classmethod
    def find_path(self, request):
        return request.split(' ')[1]

    def send_response(self, response):
        response = """HTTP/1.1 301 Moved Permanently\r\n
                   Location: /hello""".encode()
        
        self.request.sendall(response.encode())

    def handle(self):
        recieved_data = self.request.recv(1024).strip() # recieve data
        path = self.find_path(recieved_data.decode())   # find host from decoded str

        if path == '/hi':
            self.send_response(
                """
                HTTP/1.1 301 Moved Permanently\r\n
                Location: /hello
                """
            )

        elif path == '/hello':
            self.send_response(
                """
                HTTP/1.1 200 OK\r\n
                Content-Length: 12\r\n\r\n
                Hello world!
                """
            )

        else:
            self.send_response(
                """
                HTTP/1.1 404 Not Found\r\n
                Content-Type: text/plain\r\n
                content-length: 36\r\n\r\n
                The requested content does not exist
                """
            )



if __name__ == '__main__':
    HOST, PORT = 'localhost', 8000

    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()


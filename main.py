from server import CrabServer
import socketserver
import random

HOST, PORT = '0.0.0.0', random.randint(2000, 9000)
print(f'starting server for {HOST} at {PORT}')
with socketserver.ThreadingTCPServer((HOST, PORT), CrabServer) as server:
    server.serve_forever()

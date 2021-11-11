import asyncio
import basehandler

class Server:
    """
    ASGI Protocol Server
    app: An ASGI Application
    host: ip of the host
    port: server port to listen on
    connections: list of active connections
    tasks: list of scheduled tasks
    loop: asyncio event loop
    shutdown: true if the server got a signal to shutdown
    started: true if the server has created an async server

    run() - starts the server, creates a task on serve()
    async serve() - Starts the server process, asynchronously calls startup, mainloop, then shutdown
    async startup() - awaits asyncio.create_server(app, host, port, ...)
    async mainloop() - sits in a while loop that breaks if server gets the signal to disconnect, sleeps
    async shutdown() - closes sockets and cancels tasks
    """
    def __init__(self, app, host, port):
        self.app = app
        self.host = host
        self.port = port
        self.connections = []
        self.tasks = []
        self.servers = []
        self.loop = asyncio.new_event_loop()
        self.shutdown = False
        self.started = False

    def run(self):
        asyncio.run(self.serve())

    async def serve(self):
        await self.start_server()
        await self.main_loop()
        await self.shutdown()

    async def start_server(self):

        async def handler(reader, writer):
            await basehandler.handler(reader, writer, self)

        server = await asyncio.start_server(handler, self.host, self.port)
        self.servers.append(server)
        self.started = True

    async def main_loop(self):
        while not self.shutdown:
            await asyncio.sleep(0.1)

    async def stop_server(self):
        for server in self.servers:
            server.close()
            server.socket.close()
        for server in self.servers:
            await server.wait_closed()

        for conn in self.connections:
            conn.shutdown()
        await asyncio.sleep(0.1)

        if self.tasks:
            while self.tasks:
                await asyncio.sleep(0.1)

import asyncio
import basehandler
"""
For the sake of clarity I'm going to include notes that walk you through the how all of this fits together. Each module
  will have some text at the top explaining the most important things to know about that class, followed by which module
  you should read next. The purpose of this is to try to explain things in a linear sequence that follows from startup,
  to a connection received, to a request received, to the ASGI app, sending the response, and finally closing the 
  HTTP connection.
Start by reading through this class. You wont get it all immediately, but thats okay, theres a lot going on. One of the 
  main things you should take away from this file is that Server.run() starts the server by calling Server.serve 
  asynchronously. This is done to give the server class a synchronous entrance point that invokes an asynchronous method 
  that actually starts the server. 
The other important thing to know is that the actual TCP server is created in Server.start_server(). Its created 
  asynchronously by calling await asyncio.start_server(...). In Server.start_server, we define a function handler(...)
  that wraps basehandler.handler(...). That means when the TCP server created gets a connection, basehandler.handler is
  called. So after reading this file, thats where you should go nextThe purpose of this wrapper is discussed more in 
  Server.start_server's docstring, so check there for more info. 
"""


class Server:
    """
    ASGI Protocol Server Manager
    Responsible for starting and managing the ASGI Protocol Server. Keeps track of active connections and tasks.
    Call Server.run() to start the server.
    run() - starts the server, creates a task on serve()
    async serve() - Starts the server process, asynchronously calls startup, mainloop, then shutdown
    async start_server() - awaits asyncio.create_server(app, host, port, ...)
    async main_loop() - sits in a while loop that breaks if server gets the signal to disconnect, sleeps
    async stop_server() - closes sockets and cancels tasks
    """
    def __init__(self, app, host, port):
        """
        app: An ASGI Application, must be a coroutine that follows the ASGI app specifications
        host: ip of the host
        port: server port to listen on
        connections: list of active connections
        tasks: list of scheduled tasks
        loop: asyncio event loop
        servers: a list of active servers
        shutdown: true if the server got a signal to shutdown
        started: true if the server has created an async server
        """
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
        """
        Starts the server as an asyncio task
        :return: None
        """
        asyncio.run(self.serve())

    async def serve(self):
        """
        Awaits the methods that let the server do its things. See their own definitions for more info on each of
          the methods.
        :return: None
        """
        await self.start_server()
        await self.main_loop()
        await self.shutdown()

    async def start_server(self):
        """
        Defines the handler method for the asyncio server.
        Creates the server, adds it to self.servers, and sets the .started flag to True.
        The asyncio server handler takes 2 arguments, StreamReader and StreamWriter. We wrap our basehandler.handler
          method in order to pass Server to the protocol classes.
        :return: None
        """
        async def handler(reader, writer):
            await basehandler.handler(reader, writer, self)

        server = await asyncio.start_server(handler, self.host, self.port)
        self.servers.append(server)
        self.started = True

    async def main_loop(self):
        """
        Checks the shutdown flag, .shutdown, sleeping and looping if it is not set.
        This has the effect of keeping the server alive until a shutdown event is initiated.
        stop_server() is not invoked until after we break out of this loop
        :return: None
        """
        while not self.shutdown:
            await asyncio.sleep(0.1)

    async def stop_server(self):
        """
        Closes the servers, sockets, and connections.
        Waits until the remaining tasks are completed before returning
        :return: None
        """
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

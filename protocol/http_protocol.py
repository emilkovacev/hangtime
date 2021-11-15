import asyncio
from queue import Queue
from .parser import httpparser
"""
Glad to see you've made it. You look tired, maybe sit down and have a rest. Drink some water. Eat some food. 
...
Feeling better? Good, lets talk HttpProtocol. As discussed in basehandler (youre going in order right?) this class 
  defines the rules of the HTTP protocol. It also provides the send and receive methods used by ASGI. The first method
  called is .start_connection(...), which tells the ASGI Server that a connection has been made and assigns the 
  transport passed from handler(). Next data_received(...) is called from handle(). This is what actually starts 
  processing the request. It passes the data to a parser, then uses the info from the request to define the asgi scope.
  Finally it sends a signal to indicate the full message has been received, and creates a task from .do_asgi().
All do_asgi() does is awaits the ASGI application then calls shutdown once it has completed. The ASGI application will
  call .asgi_send and .asgi_receive as needed. After completing the request .asgi_receive sends an ASGI http.shutdown 
  event to the application which causes the asgi app task started in do_asgi to end, and then .shutdown is called.
  If you're confused about what asgi_send and receive are doing check out the docs for the HTTP format:
    https://asgi.readthedocs.io/en/latest/specs/www.html 
This is assuming the request wasn't and upgrade request. That'll be covered once its implemented.
"""


class HttpProtocol(asyncio.Protocol):
    def __init__(self, server, connection_lost_cb=None):
        self.server = server
        self.connection_lost_cb = connection_lost_cb
        self.transport = None
        self.server_addr = None
        self.client_addr = None
        self.parser = None
        self.partial_response = None
        self.loop = asyncio.get_event_loop()
        self.scope = {"type": "http", "asgi": {"version": "3.0", "spec_version": "2.0"},
                      "http_version": "1.1", "scheme": "http", "raw_path": None, "root_path": "", "headers": [],
                      "client": None, "server": None}
        self.message_complete_event = asyncio.Event()
        self.completed_response_flag = False
        self.asgi = None
        self.buffered_messages = Queue(0)

    def start_connection(self, transport):
        self.server.connections.append(self)
        self.transport = transport

        socket_info = transport.get_extra_info('socket')
        if socket_info is not None:
            self.client_addr = socket_info.getpeername()
            self.server_addr = socket_info.getsockname()

    def data_received(self, data: bytes) -> None:
        self.parser = httpparser.HttpParser(data, self.protocol_upgrade_callback)
        for key, value in dict({"method": self.parser.method, "path": self.parser.route,
                           "raw_path": self.parser.route.encode("ascii"),
                           "query_string": self.parser.query_string.encode("ascii"),
                           "headers": self.parser.asgi_headers, "client": self.client_addr,
                           "server": self.server_addr}).items():
            self.scope[key] = value
        self.message_complete_event.set()
        asgi = ASGIWrapper(self.server.app, self.scope, self.do_next_message, self.transport, self.message_complete_event,
                                self.completed_response_flag)

        if self.asgi is None:
            self.asgi = asgi
            task = self.loop.create_task(asgi.do_asgi())
            task.add_done_callback(self.server.tasks.remove)
            self.server.tasks.append(task)
        else: # A request is being handled
            self.buffered_messages.put((self.scope, asgi))

    def do_next_message(self):
        if self.buffered_messages.qsize() != 0:
            scope, asgi = self.buffered_messages.get()
            task = self.loop.create_task(asgi.do_asgi())
            task.add_done_callback(self.server.tasks.remove)
            self.server.tasks.append(task)
        else:
            self.shutdown()

    def protocol_upgrade_callback(self):
        pass

    def shutdown(self):
        self.transport.close()
        try:
            self.connection_lost_cb.set_result(True)
        except asyncio.exceptions.InvalidStateError:
            pass


class ASGIWrapper:
    def __init__(self, app, scope, shutdown, transport, message_event, message_flag):
        self.app = app
        self.scope = scope
        self.shutdown = shutdown
        self.transport = transport
        self.message_complete_event = message_event
        self.completed_response_flag = message_flag
        self.partial_response = None

    async def do_asgi(self):
        response = await self.app(self.scope, self.asgi_receive, self.asgi_send)
        self.shutdown()
        return

    async def asgi_send(self, message):
        more_body = True
        if message["type"] == "http.response.start":
            if self.partial_response is not None:
                print("New Message Started Before Current Message Finished!")
                print(message)
                print(self.partial_response)
                return
            status = message["status"]
            msg = STATUS_CODES[status]
            content = "HTTP/1.1 " + str(status) + " " + msg + "\r\n"
            for key, value in message["headers"]:
                content += key.decode("ascii").lower() + ": " + value.decode("ascii") + "\r\n"
            content += "X-Content-Type-Options: nosniff\r\n\r\n"
            encoded_start = content.encode()
            # NOTE: asgi docs say not to send data back to the client until
            #  at least one .response.body message has been received, but
            #  uvicorn does not do this.
            self.partial_response = encoded_start
        elif message["type"] == "http.response.body":
            if self.partial_response is None:
                print("Tried to send message body without sending headers!")
                print(message)
                return
            body = message.get("body", "")
            more_body = message.get("more_body", False)
            self.transport.write(self.partial_response + body)

        if not more_body:
            self.completed_response_flag = True
            self.message_complete_event.set()
            self.partial_response = None

    async def asgi_receive(self):
        if not self.completed_response_flag:
            await self.message_complete_event.wait()
            self.message_complete_event.clear()
        if self.completed_response_flag:
            message = {"type": "http.disconnect"}
        else:
            message = {
                "type": "http.request",
                "body": self.parser.body,
                "more_body": False
            }
        return message



STATUS_CODES = {200: "OK", 404: "NOT FOUND", 500: "???", 307: "TEMPORARY REDIRECT"}
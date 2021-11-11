import asyncio

from parser import httpparser


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

    def start_connection(self, transport):
        self.server.connections.append(self)
        self.transport = transport

        socket_info = transport.get_extra_info('socket')
        if socket_info is not None:
            self.client_addr = socket_info.getsockname()
            self.server_addr = socket_info.getpeername()

    def data_received(self, data: bytes) -> None:
        self.parser = httpparser.HttpParser(data, self.protocol_upgrade_callback)
        for key, value in dict({"method": self.parser.method, "path": self.parser.route,
                           "raw_path": self.parser.route.encode("ascii"),
                           "query_string": self.parser.query_string.encode("ascii"),
                           "headers": self.parser.headers, "client": self.client_addr,
                           "server": self.server_addr}).items():
            self.scope[key] = value
        self.message_complete_event.set()
        task = self.loop.create_task(self.do_asgi())
        task.add_done_callback(self.server.tasks.remove)
        self.server.tasks.append(task)

    def protocol_upgrade_callback(self):
        pass

    def shutdown(self):
        self.transport.close()
        try:
            self.connection_lost_cb.set_result(True)
        except asyncio.exceptions.InvalidStateError:
            pass

    async def do_asgi(self):
        response = await self.server.app(self.scope, self.asgi_send, self.asgi_receive)
        self.shutdown()
        return

    async def asgi_send(self, message):
        more_body = True
        if message["type"] == "http.response.start":
            status = message["status"]
            msg = STATUS_CODES[status]
            content = "HTTP/1.1 " + str(status) + " " + msg + "\r\n"
            for key, value in message["headers"]:
                content += key.decode("ascii").lower() + ": " + value.decode("ascii") + "\r\n"
            content += "X-Content-Type-Options: nosniff\r\n"
            encoded_start = content.encode()
            # NOTE: asgi docs say not to send data back to the client until
            #  at least one .response.body message has been received, but
            #  uvicorn does not do this.
            self.partial_response = encoded_start
        elif message["type"] == "http.response.body":
            body = message.get("body", "")
            more_body = message.get("more_body", False)
            self.transport.write(self.partial_response + body)

        if not more_body:
            self.completed_response_flag = True
            self.message_complete_event.set()

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



STATUS_CODES = {200: "OK", 400: "NOT FOUND"}
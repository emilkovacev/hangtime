PACKET = b"GET / HTTP/1.1\r\nHost: cse312.com\r\n\r\n"


class HttpParser:
    BUFFERSIZE = 1024

    def __init__(self, request, upgrade_callback):
        """
        Class to parse HTTP request from python socket class
        :param request: encoded HTTP request
        :param upgrade_callback: callback function for if this request wants to upgrade it protocol (HttpParser, socket)
        """
        self.request = request
        self.upgrade_callback = upgrade_callback
        self.content_type = ""
        self.body = {}
        self.headers = {}
        self.query_string = ""
        self.query_string_results = {}
        self.method = ""
        self.route = ""
        self.version = ""
        self.content_length = 0

        if len(self.request) == 0:
            return

        (self.method, self.route, self.version) = HttpParser.parse_status_line(request)
        self.headers = HttpParser.parse_headers(request)
        # determine if the input needs to be buffered
        content_length = int(self.headers.get("content-length", -1))

        self.full_request_bytes = request

        if content_length != -1:
            if content_length > HttpParser.BUFFERSIZE:
                raise BufferError("Content Length is larger than BUFFERSIZE")
                #self.full_request_bytes += HttpParser.buffer_input(request, content_length)
        self.content_length = content_length

        # Check for protocol upgrade
        if self.headers.get("connection") == "Upgrade" and self.headers.get("upgrade") == "websocket":
            self.upgrade_callback(self, request)
            return
        if "?" in self.route:
            self.query_string = self.route.split("?")[:-1]
            self.query_string_results = HttpParser.parse_query_string(self.query_string)
            self.route = self.route.split("?")[0]

        # parse the body of the request based on the content-type header field
        self.content_type = self.headers.get("content-type", None)
        encoded_body = self.full_request_bytes.split(b"\r\n\r\n")[1:]
        if self.content_type == "application/x-www-form-urlencoded":
            # The request body is a query string
            self.body = HttpParser.parse_query_string(encoded_body[0])
        elif self.content_type is not None:
            raise NotImplementedError("Unsupported content type")

    def __str__(self):
        x = f"{self.method} {self.route} {self.version}\r\n"
        for key, value in self.headers.items():
            x += f"{key}: {value}\r\n"
        x += "\r\n"
        for k, v in self.body.items():
            x += f"{k}: {v}\r\n"
        return x

    @property
    def root_route(self):
        return "/" + self.route.split("/")

    @staticmethod
    def buffer_input(request, content_length):
        """
        Reads in BUFFERSIZE bytes at a time until the number of bytes read is greater than [content_length]
        :param request: python socket object
        :param content_length: number of bytes in the request
        :return: bytes - all the request data
        """
        """
        bytes_read = HttpParser.BUFFERSIZE
        read_in = b""
        while bytes_read < content_length:
            read_in += request.recv(HttpParser.BUFFERSIZE)
            bytes_read += HttpParser.BUFFERSIZE
        return read_in
        """
        pass

    @staticmethod
    def parse_status_line(request_head):
        """ Parses the first line of the request
            [request_head]: the first BUFFERSIZE bytes of the request
            Returns: (method, route, version) as strings
        """
        status_line = request_head.split(b"\r\n")[0]
        method, route, version = status_line.split(b" ")
        return method.decode("ascii"), route.decode("ascii"), version.decode("ascii")

    @staticmethod
    def parse_headers(request_head):
        """
        Parses the request headers. Header Keys are converted to lowercase
        :param request_head: the first BUFFERSIZE bytes of the request
        :return: {header_key: header_value} {str: str}
        """
        pre_body = request_head.split(b"\r\n\r\n")[0]
        headers = pre_body.split(b"\r\n")[1:]
        data = {}
        for header in headers:
            kv = header.split(b":")
            data[kv[0].decode("ascii").lower().strip()] = kv[1].decode("ascii").strip()
        return data

    @staticmethod
    def parse_query_string(encoded_body):
        """
        Parses the query string. Keys are returned in lowercase
        :param encoded_body: the bytes of the query string
        :return: {key: [values, ...]}
        """
        qs_data = {}
        kvpairs = encoded_body.split(b"&")
        for pair in kvpairs:
            kv = pair.split(b"=")
            qs_data[kv[0].decode("ascii").lower().strip()] = [value.decode("ascii").strip()
                                                              for value in kv[1].split(b"+")]
        return qs_data

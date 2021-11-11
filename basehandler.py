from protocol import http_protocol
import asyncio
"""
Welcome to basehandler, traveller. As discussed before, this method is the handler for connections made to the TCP 
  server. This gets kinda sticky so bear with me. The async server handler takes a StreamReader and a 
  StreamWriter object as arguments. These are simply the interfaces the server uses to read and write data to and from
  the client. While SW and SR could technically be used by this application, instead we are going lower into asyncio.
First we need to cover asyncio.Transport and asyncio.Protocol classes. From the python docs: "At the highest level, the 
  transport is concerned with how bytes are transmitted, while the protocol determines which bytes to transmit (and to 
  some extent when)." (for more: https://docs.python.org/3/library/asyncio-protocol.html). Protocols and Transports are 
  made in pairs and associated with each other. The Protocol calls its Transport methods to send data to the client, 
  while the Transport class calls its Protocol methods to pass it data it has received. The Protocol class defines how
  the data received should be interpreted (as an HTTP request, WS frame, etc), and converts it into a usable format 
  so it can be used by the server. It also defines how to format responses from the server.
You may recall that one part of ASGI is a protocol server, that name is not a misnomer. In order to simplify defining
  the custom protocols we take the Transport object from the StreamWriter and define our own Protocol class. Note that
  the StreamReader (or a StreamReader) is still used by Transport, just not directly by the Protocol. 
From here protocol.http_protocol.HttpProtocol handles every thing else. That is where the magic really happens.
"""


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, server):
    """
    Connection handler for asynchronous TCP server.
    :param reader: reads in data from the socket
    :param writer: writes data to the socket
    :param server: the asgiserver.Server class that created this server
    :return: None
    """
    # Callback for when the connection closes
    conn_lost_callback = asyncio.get_event_loop().create_future()
    # Define the protocol as HTTP
    protocol = http_protocol.HttpProtocol(server, conn_lost_callback)
    transport = writer.transport
    # associate the protocol with the transport
    transport.set_protocol(protocol)
    # associate the transport with the protocol
    protocol.start_connection(transport)

    # get the data from the stream reader
    data = reader._buffer
    # pass the request to the Protocol class
    protocol.data_received(data)

    # when the connection closes, this is where we end up.
    await conn_lost_callback
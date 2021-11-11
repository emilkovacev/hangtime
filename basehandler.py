from protocol import http_protocol
import asyncio


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, server):

    conn_lost_callback = asyncio.get_event_loop().create_future()
    protocol = http_protocol.HttpProtocol(server, conn_lost_callback)
    transport = writer.transport
    transport.set_protocol(protocol)

    protocol.start_connection(transport)

    data = reader._buffer
    protocol.data_received(data)

    await conn_lost_callback
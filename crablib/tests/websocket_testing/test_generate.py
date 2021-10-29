import unittest

from crablib.http.websocket import generate_key
from crablib.http.response import handshake_response

class TestGenerateKey(unittest.TestCase):
    def test_mozilla_gen(self):
        sec_websocket_key = 'dGhlIHNhbXBsZSBub25jZQ=='
        expected = 's3pPLMBiTxaQ9kYGzzhZRbK+xOo='
        self.assertEqual(expected, generate_key(sec_websocket_key))

    def test_handshake(self):
        sec_websocket_key = 'dGhlIHNhbXBsZSBub25jZQ=='
        expected = b'HTTP/1.1 101 Switching Protocols\r\n'\
                   b'Upgrade: websocket\r\n'\
                   b'Connection: Upgrade\r\n'\
                   b'Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=\r\n\r\n'
        self.assertEqual(expected, handshake_response(sec_websocket_key).write_raw())


if __name__ == '__main__':
    unittest.main()


import unittest
from crablib.http.parse import Request, parse_frame, Frame, unmask, bytes_to_int, escape
import struct


class TestFormParse(unittest.TestCase):

    def test_simple_frame(self):
        test_frame = b'\x81\x06' + 'Hello!'.encode()
        expected = 'Hello!'.encode()
        actual = parse_frame(test_frame).data
        self.assertEqual(expected, actual)

    def test_xor(self):
        elem = b'\x86\xe2\x7a\x1b\x63'
        mask = b'\xab\xcd\xef\x53'
        self.assertEqual(unmask(elem, mask), b'\x2d\x2f\x95\x48\xc8')

    def test_masking_key(self):
        test_frame = b'\x81\x86' + b'\xff\xff\xff\xff' + 'Hello!'.encode()
        expected = b'\xb7\x9a\x93\x93\x90\xde'
        actual = parse_frame(test_frame).data
        self.assertEqual(expected, actual)

    def test_larger_key(self):
        test_frame = b'\x81\x7e' + b'\x01\xf4' + (b'A'*500)
        expected = b'A'*500
        frame = parse_frame(test_frame)
        actual = parse_frame(test_frame).data
        self.assertEqual(expected, actual)
        self.assertEqual(len(expected), frame.payload_len)

    def test_send_frame(self):
        frame = Frame(
            FIN=1, RSV1=0, RSV2=0, RSV3=0,
            opcode=1, MASK=0, data=b'hello!', payload_len=6
        )
        expected = b'\x81\x06hello!'
        self.assertEqual(expected, frame.write_raw())

    def test_bytes_to_int(self):
        test = b'\x23\xa7'
        self.assertEqual(bytes_to_int(test), 9127)

        test = b'\x08\x12'
        self.assertEqual(bytes_to_int(test), 2066)

    def test_escape(self):
        html = '<h1>Hello world!</h1>'
        self.assertEqual('&lt;h1&gt;Hello world!&lt;h1&gt;', escape(html))


if __name__ == '__main__':
    unittest.main()

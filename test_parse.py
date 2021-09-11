import unittest
from httplib.parse import ParseTools as pt


class TestRequest(unittest.TestCase):
    def test_no_body(self):
        http_input = 'GET /hello HTTP/1.1\r\nHost: cse312.com'
        expected_output = {
            'request_type': 'GET',
            'path': '/hello',
            'http_version': 'HTTP/1.1',
            'Host': 'cse312.com',
        }

        self.assertEqual(pt.parse_request(http_input), expected_output)

    def test_body(self):
        http_input = 'GET /hey_there HTTP/1.1\r\nHost: cse220.com\r\nContent-Length: 12\r\n\r\nHello world!'
        expected_output = {
            'request_type': 'GET',
            'path': '/hey_there',
            'http_version': 'HTTP/1.1',
            'Host': 'cse220.com',
            'Content-Length': '12',
            'body': 'Hello world!',
        }

        self.assertEqual(pt.parse_request(http_input), expected_output)


class TestResponse(unittest.TestCase):
    def test_no_body(self):
        expected_output = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0'
        output = pt.write_response(
            status_code=200,
            status_message='OK',
            headers={
                'Content-Type': 'text/plain',
                'Content-Length': 0,
            }
        )

        self.assertEqual(expected_output, output)

    def test_body(self):
        message = 'The requested content does not exist, Jesse >:('
        expected_output = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 36\r\n\r\n' + message
        output = pt.write_response(
            status_code=404,
            status_message='Not Found',
            headers={
                'Content-Type': 'text/plain',
                'Content-Length': 36,
            },
            body=message,
        )

        self.assertEqual(expected_output, output)

    def test_unicode(self):
        message = '你好！'
        expected_output = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\n' \
                          f'Content-Length: {len(message.encode())}\r\n' \
                          f'\r\n{message}'
        output = pt.write_response(
            status_code=200,
            status_message='OK',
            headers={
                'Content-Type': 'text/plain; charset=utf-8',
                'Content-Length': len(message.encode()),
            },
            body=message,
        )

        print(output)
        self.assertEqual(expected_output, output)


if __name__ == '__main__':
    unittest.main()

import unittest
from crablib.http.parse import Request, Response, FileIO, parse_request


class TestRequest(unittest.TestCase):

    def assertRequestEqual(self, requestA: Request, requestB: Request):
        self.assertEqual(requestA.request, requestB.request)
        self.assertEqual(requestA.request_type, requestB.request_type)
        self.assertEqual(requestA.path, requestB.path)
        self.assertEqual(requestA.http_version, requestB.http_version)
        self.assertEqual(requestA.headers, requestB.headers)

    def test_no_body(self):
        http_input = 'GET /hello HTTP/1.1\r\nHost: cse312.com'
        expected = Request(
            request=http_input,
            request_type='GET',
            path='/hello',
            http_version='HTTP/1.1',
            headers={'Host': 'cse312.com'}
        )

        request: Request = parse_request(http_input)
        self.assertRequestEqual(expected, request)

    def test_body(self):
        http_input = 'POST /hey_there HTTP/1.1\r\nHost: cse220.com\r\nContent-Length: 12\r\n\r\nHello world!'

        expected = Request(
            request=http_input,
            request_type='POST',
            path='/hey_there',
            http_version='HTTP/1.1',
            headers={
                'Host': 'cse220.com',
                'Content-Length': '12',
            },
            body='Hello world!',
        )

        request: Request = parse_request(http_input)
        self.assertRequestEqual(expected, request)


class TestResponse(unittest.TestCase):
    def test_no_body(self):
        expected_output = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0'
        output = Response(
            status_code=200,
            status_message='OK',
            headers={
                'Content-Type': 'text/plain',
                'Content-Length': 0,
            }
        )

        self.assertEqual(expected_output.encode(), output.write_raw())

    def test_body(self):
        message = 'The requested content does not exist, Jesse >:('
        expected_output = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 36\r\n\r\n' + message
        output = Response(
            status_code=404,
            status_message='Not Found',
            headers={
                'Content-Type': 'text/plain',
                'Content-Length': 36,
            },
            body=message.encode(),
        )

        self.assertEqual(expected_output.encode(), output.write_raw())

    def test_unicode(self):
        message = '你好！'
        expected_output = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\n' \
                          f'Content-Length: {len(message.encode())}\r\n' \
                          f'\r\n{message}'
        output = Response(
            status_code=200,
            status_message='OK',
            headers={
                'Content-Type': 'text/plain; charset=utf-8',
                'Content-Length': len(message.encode()),
            },
            body=message.encode(),
        )

        self.assertEqual(expected_output.encode(), output.write_raw())


if __name__ == '__main__':
    unittest.main()

import unittest
from crablib.http.parse import Request, Response, parse_request


class TestRequest(unittest.TestCase):

    def assertRequestEqual(self, requestA: Request, requestB: Request):
        self.assertEqual(requestA.request, requestB.request)
        self.assertEqual(requestA.request_type, requestB.request_type)
        self.assertEqual(requestA.path, requestB.path)
        self.assertEqual(requestA.http_version, requestB.http_version)
        self.assertEqual(requestA.headers, requestB.headers)
        self.assertEqual(requestA.body, requestB.body)

    def test_no_body(self):
        http_input = b'GET /hello HTTP/1.1\r\nHost: cse312.com\r\n\r\n'
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
        http_input = b'POST /hey_there HTTP/1.1\r\nHost: cse220.com\r\nContent-Length: 9\r\n\r\nHello world and stuff!'

        expected = Request(
            request=http_input,
            request_type='POST',
            path='/hey_there',
            http_version='HTTP/1.1',
            headers={
                'Host': 'cse220.com',
                'Content-Length': '9',
            },
            body=b'Hello wor',
        )

        request: Request = parse_request(http_input)
        self.assertRequestEqual(expected, request)

    def test_body2(self):
        http_input = b'POST /comment undefined\r\n' \
                     b'Host: localhost:7433\r\n' \
                     b'Content-Type: multipart/form-data; boundary=' \
                     b'---------------------------32738073535784124863642510651\r\n' \
                     b'Content-Length: 290\r\n' \
                     b'Sec-Fetch-User: ?1\r\n\r\n' \
                     b'-----------------------------32738073535784124863642510651\r\n' \
                     b'Content-Disposition: form-data; name="name"\r\n\r\n' \
                     b'Emil\r\n' \
                     b'-----------------------------32738073535784124863642510651\r\n' \
                     b'Content-Disposition: form-data; name="comment"\r\n\r\n' \
                     b':))\r\n' \
                     b'-----------------------------32738073535784124863642510651--'

        request: Request = parse_request(http_input)
        print('***')
        print(request.body.decode())
        print('***')


class TestResponse(unittest.TestCase):
    def test_no_body(self):
        expected_output = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n'
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
                          f'Content-Length: {len(message.encode())}\r\n\r\n' \
                          f'{message}'
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

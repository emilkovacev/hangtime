import unittest
from crablib.http.parse import Request, parse_request
from views import form


class TestFormParse(unittest.TestCase):

    def test_no_body(self):
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

        print(form(request))
        # self.assertEqual(expected, request)


if __name__ == '__main__':
    unittest.main()

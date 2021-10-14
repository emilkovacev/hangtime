import unittest
from crablib.http.parse import Request, parse_request, parse_form


class TestFormParse(unittest.TestCase):

    def test_text_form(self):
        http_input = b'POST /comment HTTP/1.1\r\n' \
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

        print(parse_form(request))
        # self.assertEqual(expected, request)

    def test_image_form(self):
        http_input = b'POST /form-path HTTP/1.1\r\n' \
                     b'Content-Length: 9937\r\n' \
                     b'Content-Type: multipart/form-data; boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n' \
                     b'------WebKitFormBoundarycriD3u6M0UuPR1ia\r\n' \
                     b'Content-Disposition: form-data; name="commenter"\r\n\r\n' \
                     b'Jesse\r\n' \
                     b'------WebKitFormBoundarycriD3u6M0UuPR1ia\r\n' \
                     b'Content-Disposition: form-data; name="upload"; filename="discord.png"\r\n' \
                     b'Content-Type: image/png\r\n\r\n' \
                     b'<bytes_of_the_file>\r\n' \
                     b'------WebKitFormBoundarycriD3u6M0UuPR1ia--'

        request: Request = parse_request(http_input)
        print(parse_form(request))


if __name__ == '__main__':
    unittest.main()

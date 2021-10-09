import re
import socketserver

from crablib.http.parse import Request, parse_request, FileIO
from crablib.http.response import http_200, http_301, http_404
from crablib.querygen.reader import read_query

from urls import urls, Path


class CrabServer(socketserver.BaseRequestHandler):
    def send_response(self, response: bytes):
        self.request.sendall(response)
        return

    def handle(self):
        request: str = self.request.recv(1024).decode()
        print(repr(request))
        data: Request = parse_request(request)

        response_404 = http_404(
            content_type='text/html',
            content=FileIO('crablib/error_templates/404.html').read()
        )

        item: Path
        for item in urls:
            match = re.match(item.regex, data.path)
            if match and item.path:
                try:
                    self.send_response(http_200(
                        content_type=item.mimetype,
                        content=FileIO(item.path).read()
                    ).write_raw())
                    return
                except FileNotFoundError:
                    self.send_response(response_404.write_raw())

            elif match:
                try:
                    self.send_response(http_200(
                        content_type=item.mimetype,
                        content=FileIO(match.group(1)).read()
                    ).write_raw())
                    return
                except FileNotFoundError:
                    self.send_response(response_404.write_raw())
        self.send_response(response_404.write_raw())
        return

        # if re.match('^/$', path):
        #     file = http_200('text/html', FileIO('html/index.html').read(), 'utf-8').write_raw()
        #     self.send_response(file)
        #
        # elif re.match('^/images/[^.]+\\.\\w+$', path):
        #     pass
        #
        # elif re.match('^/images/(?P<title>[^. ]+)\\.(?P<file>(png|jpg|jpeg))+$', path):
        #     filename = re.match("[^/]+.$", path)
        #     file_ext = re.match("(?<=[.]).+$", path)
        #
        #     try:
        #         file = http_200(f'image/{file_ext.string}', image(f'image/{filename}'))
        #         self.send_response(file)
        #     except FileNotFoundError:
        #         file = http_404('text/html', read('crablib/error_templates/404.html'))
        #         self.send_response(file)
        # elif re.match('^/images?.+', path):
        #     arguments = read_query(path)
        #     try:
        #         file = http_200(f'text/html', html('html/index.html', arguments))
        #         self.send_response(file)
        #     except FileNotFoundError:
        #         file = http_404('text/html', read('crablib/error_templates/404.html'))
        #         self.send_response(file)
        #
        # elif re.match('^/style/style.css$', path):
        #     file = http_200('text/css', read('style/style.css'), 'utf-8')
        #     self.send_response(file)
        #
        # elif re.match('^/script.script.script$', path):
        #     file = http_200('text/javascript', read('script/script.script'), 'utf-8')
        #     self.send_response(file)
        #
        # elif re.match('^/utf.txt$', path):
        #     file = http_200('text/html', read('utf.txt'), 'utf-8')
        #     self.send_response(file)
        #
        # elif re.match('^/hello$', path):
        #     response = http_200('text/plain', text('Hello world!'))
        #     self.send_response(response)
        #
        # elif re.match('^/hi$', path):
        #     response = http_301('/hello')
        #     self.send_response(response)
        #
        # else:
        #     file = http_404('text/html', read('crablib/error_templates/404.html'))
        #     self.send_response(file)

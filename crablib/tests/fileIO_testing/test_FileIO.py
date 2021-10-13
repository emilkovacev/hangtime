import unittest
from crablib.http.parse.parse import FileIO
from crablib.htmlgen.generate import generate_html


class TestRequest(unittest.TestCase):

    def test_image(self):
        path = '../../../images/big-yoshi.jpg'

        fileA = FileIO(path).read()
        fileB: bytes
        with open(path, 'rb') as f:
            fileB = f.read()

        self.assertEqual(fileA, fileB)

    def test_utf8(self):
        path = '../../../utf.txt'
        fileA = FileIO(path).read()
        with open(path, 'rb') as f:
            fileB = f.read()

        self.assertEqual(fileA, fileB)

    def test_html(self):
        path = '../../../html/images.html'
        args = {'name': 'Emil', 'images': ['penguin.jpg', 'cat.jpg', 'dog.jpg']}
        fileA = FileIO(path, args).read()

        fileB = generate_html(path, args).encode()
        html = '<!DOCTYPE html><html><head><link rel="stylesheet" href="/style/style.css"></head><body><div>Emil'  \
               '<img src="penguin.jpg"/><img src="cat.jpg"/><img src="dog.jpg"/>'                   \
               '</div></body></html>'.encode()

        self.assertEqual(fileB, fileA)
        self.assertEqual(html, fileA)


if __name__ == '__main__':
    unittest.main()

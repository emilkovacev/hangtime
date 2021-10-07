import unittest
from crablib.htmlgen.generate import generate_html
from crablib.querygen.reader import read_query


class TestHTMLGen(unittest.TestCase):
    def test_body(self):
        args = read_query('/images?images=kitten+flamingo&name=Emil')
        # find absolute path of image name in /images
        for i in range(len(args['images'])):
            args['images'][i] = '/images/' + args['images'][i] + '.jpg'
        html = generate_html('../templates/obj1.html', args)
        test = '<!DOCTYPE html><html><body><h1>Hello Emil!</h1><img src="/images/kitten.jpg"/>' \
               '<img src="/images/flamingo.jpg"/></body></html>'
        self.assertEqual(test, html)


if __name__ == '__main__':
    unittest.main()

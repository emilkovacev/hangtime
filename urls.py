from crablib.http.path import Path

urls = [
    Path('^/$', 'text/html', path='html/index.html'),
    Path('^\\/(images\\/[^.]+\\.(jpg|jpeg))$', 'image/jpeg'),
    Path('^\\/(style\\/[^.]+\\.css)$', 'text/css'),
    Path('^\\/(script\\/[^.]+\\.js)$', 'text/javascript'),
]

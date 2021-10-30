from crablib.http.path import Path
from views import chat, uploads


urls = [
    Path('^/$', uploads.index),
    Path('^/script/websocket.js$', chat.websocketjs),
    Path('^/websocket$', chat.websocket),
    Path('^/yoshi$', uploads.yoshi),
    Path('^\\/(images\\/[^.]+\\.(jpg|jpeg))$', uploads.img),
    Path('^\\/(style\\/[^.]+\\.css)$', uploads.css),
    Path('^\\/(script\\/[^.]+\\.js)$', uploads.js),
]

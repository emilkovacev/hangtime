from crablib.http.path import Path
from views import chat, uploads


urls = [
    Path('^/$', uploads.index),
    Path('^/uploads$', uploads.uploads),
    Path('^/script/websocket.js$', chat.websocketjs),
    Path('^/websocket$', chat.websocket),
    Path('^/yoshi$', uploads.yoshi),
    Path('^\\/(images\\/[^.]+\\.(jpg|jpeg))$', uploads.img),
    Path('^\\/(style\\/[^.]+\\.css)$', uploads.css),
    Path('^\\/(script\\/[^.]+\\.js)$', uploads.js),
    Path('^/(images\\?[^?]+)$', uploads.images),
    Path('^/comment$', uploads.form_upload),
    Path('^/image-upload$', uploads.image_upload),
]

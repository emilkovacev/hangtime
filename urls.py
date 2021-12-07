from crablib.http.path import Path
from views import static, chat, auth

urls = [
    Path('^/$', static.index),

    # login paths
    Path('^/login$', auth.login),
    Path('^/register$', auth.register),
    Path('^/logout', auth.logout),

    # chat paths
    Path('^/chat$', chat.index),
    Path('^/script/websocket.js$', chat.websocketjs),
    Path('^/websocket$', chat.websocket),

    # default paths
    Path('^/(images/[^.]+.(jpg|jpeg))$', static.img),
    Path('^/(style/[^.]+.css)$', static.css),
    Path('^/(script/[^.]+.js)$', static.js),
]

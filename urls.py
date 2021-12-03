from crablib.http.path import Path
from views import static, chat, api, auth

urls = [
    Path('^/$', static.index),

    # login paths
    Path('^/login$', auth.login),
    Path('^/register$', auth.register),
    Path('^/auth$', auth.auth),

    # chat paths
    Path('^/chat$', chat.index),
    Path('^/script/websocket.js$', chat.websocketjs),
    Path('^/websocket$', chat.websocket),

    # default paths
    Path('^/(images/[^.]+.(jpg|jpeg))$', static.img),
    Path('^/(style/[^.]+.css)$', static.css),
    Path('^/(script/[^.]+.js)$', static.js),

    # RESTFUL API paths
    Path('^/users$', api.routing),
    Path('^/users/\\w+$', api.param_routing)
]

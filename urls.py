from crablib.http.path import Path
from views import static, chat, api


urls = [
    Path('^/$', static.index),

    # websocket paths
    Path('^/script/websocket.js$', chat.websocketjs),
    Path('^/websocket$', chat.websocket),

    # default paths
    Path('^/yoshi$', static.yoshi),
    Path('^/(images/[^.]+.(jpg|jpeg))$', static.img),
    Path('^/(style/[^.]+.css)$', static.css),
    Path('^/(script/[^.]+.js)$', static.js),

    # RESTFUL API paths
    Path('^/users$', api.routing),
    Path('^/users/\\w+$', api.param_routing)
]

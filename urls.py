from crablib.http.path import Path
from views import static, chat, auth, calendar

urls = [
    Path('^/$', static.index),

    # login paths
    Path('^/login$', auth.login),
    Path('^/register$', auth.register),
    Path('^/logout', auth.logout),

    # chat paths
    Path('^/chat$', chat.index),
    Path('^/websocket$', chat.websocket),

    # calendar paths
    Path('^/event$', calendar.event),
    Path('^/calsocket$', calendar.websocket),

    # default paths
    Path('^/(images/[^.]+.(jpg|jpeg))$', static.img),
    Path('^/(style/[^.]+.css)$', static.css),
    Path('^/(script/[^.]+.js)$', static.js),
]

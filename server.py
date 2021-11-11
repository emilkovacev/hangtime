from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from views import calendar, chatapp, auth

import uvicorn


routes = [
    Route('/', endpoint=calendar.index),
    Route('/chat', endpoint=chatapp.chat),
    Route('/login', endpoint=auth.login)
]

app = Starlette(debug=True, routes=routes)  # CHANGE TO FALSE AT DEPLOYMENT
app.mount('/static', StaticFiles(directory='static'), name='static')


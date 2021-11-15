from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import FileResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

import os

from asgiserver import Server
"""
If you havent already, read the specifications for ASGI: https://asgi.readthedocs.io/en/latest/specs/main.html, its not
  long. This script creates a simple Starlette application with a single route to the root page. Since you have read the 
  ASGI specs by now, you know that ASGI is made up of two parts: a protocol server and an application. 
  You may notice that there is not a function defined in the ASGI format (async def app(scope, send, receive). Starlette
  takes care of that by defining a __call__ method that follows the format which makes the Startlette application 
  our ASGI app.
"""


def index(request):
    return FileResponse("templates/calendar.html")


def style(req):
    return FileResponse("static/css/style.css")


def startup():
    print("Started")


routes = [
    Route("/", index),
    Mount('/static', app=StaticFiles(directory="static"), name="static"),
]


def main():
    app = Starlette(debug=True, routes=routes, on_startup=[startup])
    server = Server(app, "127.0.0.1", "8080")
    # This starts the server task
    server.run()


if __name__ == "__main__":
    main()
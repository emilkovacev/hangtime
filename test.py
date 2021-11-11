from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import FileResponse
from asgiserver import Server


def index(request):
    return FileResponse("index.html")


def startup():
    print("Started")


routes = [
    Route("/", index)
]


def main():
    app = Starlette(debug=True, routes=routes, on_startup=[startup])
    server = Server(app, "localhost", "8080")
    server.run()


if __name__ == "__main__":
    main()

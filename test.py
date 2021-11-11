from starlette.responses import FileResponse
from asgiserver import Server


async def app(scope, send, receive):
    assert scope['type'] == "http"
    response = FileResponse("index.html")
    await response(scope, receive, send)


def main():
    server = Server(app, "localhost", "8080")
    server.run()


if __name__ == "__main__":
    main()


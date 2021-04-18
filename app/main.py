from helpers.db import update_rating

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount, WebSocketRoute


def homepage(request):
    return PlainTextResponse("Hello, world!")


async def game_finished(request):
    body = request.json()
    winner = body["winner"]
    loser = body["loser"]

    update_rating(winner, loser)


async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text("Hello, websocket!")
    await websocket.close()


def startup():
    print("Ready to go")


routes = [
    Route("/", homepage),
    Route("/game", game_finished, methods=["POST"]),
    WebSocketRoute("/ws", websocket_endpoint),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])

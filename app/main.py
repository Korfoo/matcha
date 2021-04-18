import logging

from app.helpers.db import update_rating

from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount, WebSocketRoute

logger = logging.getLogger("matcha")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Matcha testing page</title>
    </head>
    <body>
        <h1>Matcha Test</h1>
        <form action="" onsubmit="">
            <label>id: <input type="text" id="id" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">queue</button>
            <hr>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var user = document.getElementById("id")
                ws = new WebSocket("ws://localhost:8000/queue?user=" + user.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


def homepage(request):
    return HTMLResponse(html)


async def game_finished(request):
    body = request.json()
    winner = body["winner"]
    loser = body["loser"]

    update_rating(winner, loser)


async def queue(websocket):
    await websocket.accept()
    user_id = websocket.query_params["user"]
    logger.debug(f"User {user_id} to be put in queue.")
    await websocket.send_text(f"User {user_id} to be put in queue.")
    await websocket.close()


def startup():
    print("Ready to go")

routes = [
    Route("/", homepage),
    Route("/game", game_finished, methods=["POST"]),
    WebSocketRoute("/queue", queue),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])

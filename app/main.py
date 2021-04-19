import logging

from app.helpers.db import update_rating, add_user, update_rating, get_user, update_games_played
from app.helpers.elo import calculate_new_rating

from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

logger = logging.getLogger("matcha")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

async def game_finished(request):
    body = request.json()
    winner = get_user(body["winner"])
    loser = get_user(body["loser"])

    new_ratings = calculate_new_rating(winner["rating"], loser["rating"], 30, 0)

    await update_rating(body["winner"], new_ratings[0])
    await update_rating(body["loser"], new_ratings[1])
    await update_games_played(body["winner"])
    await update_games_played(body["loser"])



async def queue(websocket):
    # Get the id of the user from the query parameters
    user_id = websocket.query_params["user"]
    if not user_id:
        await websocket.close(code=1008)

    await websocket.accept()

    # Add user to databaase as guest if not yet registered
    user = await get_user(user_id)
    if not user:
        user = await add_user(user_id, "guest")

    # Add user to the queue
    match = await search_match(user)

    # Return room  id to user when match is found
    logger.debug(user["rating"])


    await websocket.send_json(match)
    await websocket.close()


def startup():
    logger.info("Fueled up and ready to roll out!")

routes = [
    Route("/game", game_finished, methods=["POST"]),
    WebSocketRoute("/queue", queue),
    Mount('/', app=StaticFiles(directory='static'), name="static"),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])

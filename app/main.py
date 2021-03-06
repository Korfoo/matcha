import logging

from app.helpers.db import update_rating, add_user, update_rating, get_user, update_games_played
from app.helpers.elo import calculate_new_rating
from app.helpers.matchmaking import search_match
from app.helpers.config import config

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

logger = logging.getLogger("matcha")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

async def game_finished(request):
    body = await request.json()
    winner = await get_user(body["winner"])
    loser = await get_user(body["loser"])

    new_ratings = calculate_new_rating(winner["rating"], loser["rating"], 30, 0)

    await update_rating(body["winner"], new_ratings[0])
    await update_rating(body["loser"], new_ratings[1])
    await update_games_played(body["winner"])
    await update_games_played(body["loser"])

    return JSONResponse(new_ratings)

async def queue(websocket):
    # Get the id of the user from the query parameters
    user_id = websocket.query_params["user"]
    if not user_id:
        await websocket.close(code=1008)

    await websocket.accept()

    user = await get_user(user_id)

    # Add user to databaase as guest if not yet registered
    if not user:
        user = await add_user(user_id, "guest")

    logger.debug(f"Adding {user} to the queue.")
    # Add user to the queue
    match = await search_match(user)

    # Return room  id to user when match is found
    await websocket.send_json(match)
    await websocket.close()


def startup():
    logger.info("Fueled up and ready to roll out!")

routes = [
    Route("/game", game_finished, methods=["POST"]),
    WebSocketRoute("/queue", queue),
]

if config.environment == "debug":
    routes.append(Mount('/', app=StaticFiles(directory='static'), name="static"))

app = Starlette(debug=True, routes=routes, on_startup=[startup])

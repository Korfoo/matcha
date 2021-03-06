import aioredis
import logging
import json

logger = logging.getLogger("matcha")

async def update_rating(user_id: str, rating: int):
    conn = await aioredis.create_connection("redis://redis", encoding="utf-8")
    await conn.execute("JSON.SET", user_id, ".rating", rating)
    conn.close()


async def update_games_played(user_id: str):
    conn = await aioredis.create_connection("redis://redis", encoding="utf-8")
    await conn.execute("JSON.NUMINCRBY", user_id, ".games_played", 1)
    conn.close()



async def add_user(user_id: str, username: str) -> dict:
    conn = await aioredis.create_connection("redis://redis", encoding="utf-8")

    user = {"id": user_id, "username": username, "rating": 800, "games_played": 0}
    logger.debug(f"Adding {user} to database")
    await conn.execute("JSON.SET", user_id, ".", json.dumps(user))
    conn.close()
    await conn.wait_closed()

    return user

async def get_user(user_id: str) -> dict:
    conn = await aioredis.create_connection("redis://redis", encoding="utf-8")

    user = await conn.execute("JSON.GET", user_id)

    conn.close()
    await conn.wait_closed()

    if user:
        return json.loads(user)
    else:
        return None


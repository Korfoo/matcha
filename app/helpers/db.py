import aioredis
import logging
import json

logger = logging.getLogger("matcha")

async def update_rating(user_id: str, rating: int):
    conn = await aioredis.create_connection("redis://redis", encoding="utf-8")
    ok = await conn.execute("JSON.NUMINCRBY", user_id, ".rating", rating)


async def add_user(user_id: str, username: str) -> dict:
    conn = await aioredis.create_connection("redis://redis", encoding="utf-8")

    user = {"username": username, "rating": 800, "games_played": 0}
    logger.debug(f"Adding {user} to database")
    ok = await conn.execute("JSON.SET", user_id, ".", json.dumps(user))

    return user

async def get_user(user_id: str) -> dict:
    conn = await aioredis.create_connection("redis://redis", encoding="utf-8")

    user = await conn.execute("JSON.GET", user_id)

    if not user:
        user = {"id": user_id, "rating": 800}
        logger.debug(f"Adding {user_id} to db with 800 rating")
        ok = await conn.execute("JSON.SET", user_id, ".", json.dumps(user))

    conn.close()
    await conn.wait_closed()

    return user
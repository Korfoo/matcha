import logging

import aioredis

logger = logging.getLogger("matcha")

# Redis /1 is used for matchmaking pool
# Redis /2 is used to put matches found


async def _put_user(user_id: str, user_rating: int):
    redis = await aioredis.create_redis("redis://0.0.0.0:6379/1")

    await redis.zadd("matchmaking_pool", user_rating, user_id)
    await redis.zadd("matchmaking_time", time.time(), user_id)

    redis.close()
    await redis.wait_closed()



async def _get_match(user_id: str):
    redis = await aioredis.create_redis("redis://0.0.0.0:6379/2")

    # Subscribe to the matches table
    res = await redis.subscribe("matches")

    ch = res[0]

    # Keep waiting for messages until a match is found for the user
    while await ch.wait_message():
        msg = await ch.get_json()

        if user_id in [msg["player_1"], msg["player_2"]]:
            await redis.unsubscribe("matches")

    return msg



async def search_match(user: dict) -> dict:
    # Add user to the queue
    await _put_user(user["id"], user["rating"])
    logger.debug(f"{user["username"]} added to the queue.")

    # Wait for match to be found
    match = await _get_match()
    logger.debug(f"Match found: {match}")

    return match

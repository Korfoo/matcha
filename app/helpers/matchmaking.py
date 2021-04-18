import logging

import aioredis

logger = logging.getLogger("matcha")


async def put_user(user_id: str, user_rating: int):
    redis = await aioredis.create_redis("redis://0.0.0.0:6379/1")

    await redis.zadd("matchmaking_pool", user_rating, user_id)
    await redis.zadd("matchmaking_time", time.time(), user_id)
    logger.debug(f"Added {user_id} with {user_rating} rating to the matchmaking pool.")

    redis.close()
    await redis.wait_closed()


def test_debug_log():
    logger.debug("SOMETHINGSOMETHINGSOMETHING")
import logging

import aioredis

from app.db.schemas import User

logger = logging.getLogger(__name__)


async def put_user(user_id: str, user_rating: int):
    redis = await aioredis.create_redis("redis://0.0.0.0:6379/1")

    await redis.zadd("matchmaking_pool", user.rating, user.id)
    await redis.zadd("matchmaking_time", time.time(), user.id)
    logger.debug(f"Added {user_id} with {user_rating} rating to the matchmaking pool.")

    redis.close()
    await redis.wait_closed()

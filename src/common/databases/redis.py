"""
Redis client.
"""
from redis import asyncio as aioredis
from src.base_settings import base_settings


class RedisClient:
    """
    Provide singleton client for Redis.
    """

    redis: aioredis.Redis = None

    @classmethod
    def get_or_create(cls) -> aioredis.Redis:
        """
        Provide get or create class method to get redis client instance.

        Returns:
            Redis client instance.
        """
        if cls.redis is None:
            cls.redis = aioredis.from_url(
                f'redis://{base_settings.redis.host}:{base_settings.redis.port}',
                decode_responses=True,
            )
        return cls.redis


def get_redis_client() -> aioredis.Redis:
    """
    Provide wrapper for getting Redis client.

    Returns:
        Redis client instance.
    """
    return RedisClient.get_or_create()

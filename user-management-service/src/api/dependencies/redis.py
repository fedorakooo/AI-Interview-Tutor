from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from src.config import settings
from src.domain.abstractions.redis.redis_client import AbstractRedisClient
from src.infrastructure.redis.redis_client import RedisClient


@lru_cache
def get_redis() -> Redis:
    return Redis(
        host=settings.redis_settings.host,
        port=settings.redis_settings.port,
        username=settings.redis_settings.username,
        password=settings.redis_settings.password,
        decode_responses=settings.redis_settings.decode_responses,
    )


def get_redis_client(
    redis: Annotated[Redis, Depends(get_redis)],
) -> AbstractRedisClient:
    return RedisClient(
        redis=redis,
    )

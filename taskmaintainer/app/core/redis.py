from typing import Optional

import aioredis

from core.settings import settings


class Redis:
    _instance: Optional[aioredis.Redis] = None

    def __new__(cls) -> aioredis.Redis:
        if not cls._instance:
            cls.connect()
        return cls._instance
    
    @classmethod
    def connect(cls) -> None:
        cls._instance = aioredis.from_url(
            settings.REDIS.URL,
        )
    
    @classmethod
    async def close(cls) -> None:
        if cls._instance:
            await cls._instance.close()
            cls._instance = None


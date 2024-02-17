from redis import Redis    # type: ignore

from src.infrastructure.inmemory.service import RedisService


class RedisProvider:
    def __init__(self, pool: Redis):
        self.pool = pool

    async def provide_db(self):
        return RedisService(self.pool)


def in_memory_provider() -> None:
    pass

from redis import Redis      # type: ignore


def init_redis_pool(host: str) -> Redis:
    pool = Redis(host=host, db=1, encoding="utf-8", decode_responses=True)
    return pool

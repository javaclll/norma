import redis

from core import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    password=settings.REDIS_PASSWORD,
    port=int(settings.REDIS_PORT),
)

redis_client = redis.Redis(connection_pool=pool)

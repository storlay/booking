from src.config import settings
from src.connectors.redis_connector import RedisManager


redis_manager = RedisManager(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
)

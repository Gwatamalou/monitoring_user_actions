from .db import db_redis
from .services import RedisServices

def get_redis_client():
    return db_redis.get_client()


def get_redis_services():
    return RedisServices()
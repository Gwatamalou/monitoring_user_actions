from src.db import db_redis

class RedisRepositoryBase:
    def __init__(self):
        self.client = db_redis.get_client()

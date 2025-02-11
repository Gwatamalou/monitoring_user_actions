import redis


class RedisDB:
    def __init__(self):
        self.client = redis.Redis(host="redis", port="6379", decode_responses=True)

    def get_client(self):
        return self.client


db_redis = RedisDB()

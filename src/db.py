import redis


class RedisDB:
    def __init__(self):
        self.client = redis.Redis(host="127.0.0.1", port="6379", decode_responses=True)

    def get_client(self):
        return self.client


db_redis = RedisDB()

import json
from .base import RedisRepositoryBase



class RedisCache(RedisRepositoryBase):

    def cache_user_profile(self, user_id: int, profile_data: dict, expire_time: int=300):
        self.client.setex(f"user_cache:{user_id}", expire_time, json.dumps(profile_data))

    def get_cache_user_profile(self, user_id: int):
        data = self.client.get(f"user_cache:{user_id}")
        return json.loads(data) if data else None

    def invalidate_cache(self, user_id: int):
        self.client.delete(f"user_cache:{user_id}")
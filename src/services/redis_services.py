from src.repositories import RedisRepository, RedisCache
from src.schemas import User

class RedisServices:

    def __init__(self):
        self.repository = RedisRepository()
        self.cache = RedisCache()

    """
    Redis Repository
    """
    def log_event(self, user_id: int, event_type: str, metadata: dict):
        self.repository.log_event(user_id=user_id, event_type=event_type, metadata=metadata)

    def save_user_profile(self, user_id: int, name: str, age: int, city: str):
        self.repository.save_user_profile(user_id=user_id, name=name, age=age, city=city)
        self.cache.invalidate_cache(user_id=user_id)

    def track_unique_user(self, user_id: int):
        self.repository.track_unique_user(user_id=user_id)

    def update_user_activity(self, user_id: int):
        self.repository.update_user_activity(user_id=user_id)

    def get_user_profile(self, user_id):
        return self.repository.get_user_profile(user_id=user_id)

    def increment_statistics_bulk(self, event_type: str, user_id:int):
        events = [{
            "event_type": event_type,
            "user_id": user_id
        }]
        self.repository.increment_statistics_bulk(events=events)

    def increment_event_count(self, event_type: str):
        self.repository.increment_event_count(event_type=event_type)

    def get_event_count(self, event_type: str):
        return self.repository.get_event_count(event_type=event_type)

    def increment_user_activity(self, user_id: int):
        self.repository.increment_user_activity(user_id=user_id)

    def get_user_activity(self, user_id: int):
        return self.repository.get_user_activity(user_id=user_id)

    def get_redis_stats(self):
        return self.repository.get_redis_stats()

    """
    Redis Cache
    """
    def cache_user_profile(self, user_id: int, profile_data: dict, expire_time: int=300):
        self.cache.cache_user_profile(user_id=user_id, profile_data=profile_data, expire_time=expire_time)

    def get_cache_user_profile(self, user_id: int) -> User:
        cached_profile = self.cache.get_cache_user_profile(user_id=user_id)
        return cached_profile

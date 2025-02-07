import json
from src.schemas import Event, User, UserIn, UserOut
from .base import RedisRepositoryBase



class RedisRepository(RedisRepositoryBase):

    def log_event(self, user_id: int, event_type: str, metadata: dict, expire=3000):
        event = Event(
            user_id=user_id,
            event_type=event_type,
            metadata=metadata
        )
        self.client.lpush("event_queue", json.dumps(event.model_dump()))
        self.client.expire("event_queue", expire)


    def save_user_profile(self, user_id: int, name: str, age: int, city: str):
        print("FFFFFFFFF SAVE")
        user = UserIn(
            user_id=user_id,
            name=name,
            age=age,
            city=city
        )
        self.client.hset(f"user:{user_id}", mapping=user.model_dump())

    def get_user_profile(self, user_id):
        return self.client.hgetall(f"user:{user_id}")

    def track_unique_user(self, user_id: int):
        self.client.sadd(f"unique_user", user_id)


    def update_user_activity(self, user_id: int):
        self.client.zincrby("user_activity", 1, user_id)

    def increment_statistics_bulk(self, events: list[dict]):
        with self.client.pipeline() as pipe:
            for event in events:
                pipe.hincrby("event_counts", event["event_type"], 1)
                pipe.zincrby("user_activity", 1, event["user_id"])
            pipe.execute()

    def increment_event_count(self, event_type: str):
            self.client.hincrby("event_counts", event_type, 1)


    def get_event_count(self, event_type: str):
        return self.client.hget("event_counts", event_type)

    def increment_user_activity(self, user_id: int):
        self.client.zincrby("user_activity", 1, user_id)

    def get_user_activity(self, user_id: int):
        return self.client.zscore("user_activity", user_id)

    def get_redis_stats(self):
        stats = self.client.info()
        return {
            "connected_clients": stats["connected_clients"],
            "used_memory": stats["used_memory_human"],
            "total_commands_processed": stats["total_commands_processed"],
            "uptime_in_seconds": stats["uptime_in_seconds"],
            "instantaneous_ops_per_sec": stats["instantaneous_ops_per_sec"],
        }


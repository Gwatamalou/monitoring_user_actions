import json
from src.schemas import Event, User, UserIn, UserOut
from .base import RedisRepositoryBase


class RedisRepository(RedisRepositoryBase):
    """
    Репозиторий для работы с данными в Redis, включая обработку событий,
    сохранение и получение профилей пользователей, а также сбор статистики.
    Наследуется от базового класса RedisRepositoryBase.
    """

    def log_event(self, user_id: int, event_type: str, metadata: dict, expire=3000):
        """
        Записывает событие в очередь событий Redis.

        :param user_id: Идентификатор пользователя, с которым связано событие.
        :param event_type: Тип события.
        :param metadata: Дополнительные данные о событии в виде словаря.
        :param expire: Время жизни очереди событий в Redis (по умолчанию 3000 секунд).
        """
        event = Event(
            user_id=user_id,
            event_type=event_type,
            metadata=metadata
        )
        self.client.lpush("event_queue", json.dumps(event.model_dump()))
        self.client.expire("event_queue", expire)

    def save_user_profile(self, user_id: int, name: str, age: int, city: str):
        """
        Сохраняет профиль пользователя в Redis.

        :param user_id: Идентификатор пользователя.
        :param name: Имя пользователя.
        :param age: Возраст пользователя.
        :param city: Город пользователя.
        """
        user = UserIn(
            user_id=user_id,
            name=name,
            age=age,
            city=city
        )
        self.client.hset(f"user:{user_id}", mapping=user.model_dump())

    def get_user_profile(self, user_id):
        """
        Получает профиль пользователя из Redis.

        :param user_id: Идентификатор пользователя.
        :return: Словарь с данными пользователя.
        """
        return self.client.hgetall(f"user:{user_id}")

    def track_unique_user(self, user_id: int):
        """
        Добавляет пользователя в множество уникальных пользователей в Redis.

        :param user_id: Идентификатор пользователя.
        """
        self.client.sadd(f"unique_user", user_id)

    def update_user_activity(self, user_id: int):
        """
        Обновляет активность пользователя в Redis (увеличивает значение на 1).

        :param user_id: Идентификатор пользователя.
        """
        self.client.zincrby("user_activity", 1, user_id)

    def increment_statistics_bulk(self, events: list[dict]):
        """
        Увеличивает статистику для нескольких событий и пользователей в Redis.

        :param events: Список событий, для которых нужно обновить статистику.
        """
        with self.client.pipeline() as pipe:
            for event in events:
                pipe.hincrby("event_counts", event["event_type"], 1)
                pipe.zincrby("user_activity", 1, event["user_id"])
            pipe.execute()

    def increment_event_count(self, event_type: str):
        """
        Увеличивает счетчик для конкретного типа события.

        :param event_type: Тип события, для которого нужно увеличить счетчик.
        """
        self.client.hincrby("event_counts", event_type, 1)

    def get_event_count(self, event_type: str):
        """
        Получает количество событий для конкретного типа события.

        :param event_type: Тип события.
        :return: Количество событий данного типа.
        """
        return self.client.hget("event_counts", event_type)

    def increment_user_activity(self, user_id: int):
        """
        Увеличивает активность пользователя на 1.

        :param user_id: Идентификатор пользователя.
        """
        self.client.zincrby("user_activity", 1, user_id)

    def get_user_activity(self, user_id: int):
        """
        Получает уровень активности пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Уровень активности пользователя.
        """
        return self.client.zscore("user_activity", user_id)

    def get_redis_stats(self):
        """
        Получает статистику Redis (например, количество подключений, использованную память).

        :return: Словарь со статистическими данными Redis.
        """
        stats = self.client.info()
        return {
            "connected_clients": stats["connected_clients"],
            "used_memory": stats["used_memory_human"],
            "total_commands_processed": stats["total_commands_processed"],
            "uptime_in_seconds": stats["uptime_in_seconds"],
            "instantaneous_ops_per_sec": stats["instantaneous_ops_per_sec"],
        }

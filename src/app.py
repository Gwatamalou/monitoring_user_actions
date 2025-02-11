from src.repositories import RedisRepository, RedisCache
from src.schemas import User


class RedisServices:
    """
    Сервис для работы с Redis репозиторием и кэшем.
    Предоставляет методы для обработки событий, сохранения и получения данных пользователей,
    а также работы с кэшем.
    """

    def __init__(self):
        """
        Инициализирует сервис, создавая экземпляры репозитория Redis и кэша.
        """
        self.repository = RedisRepository()
        self.cache = RedisCache()

    """
    Redis Repository
    """

    def log_event(self, user_id: int, event_type: str, metadata: dict):
        """
        Записывает событие в очередь событий.

        :param user_id: Идентификатор пользователя, с которым связано событие.
        :param event_type: Тип события.
        :param metadata: Дополнительные данные события.
        """
        self.repository.log_event(user_id=user_id, event_type=event_type, metadata=metadata)

    def save_user_profile(self, user_id: int, name: str, age: int, city: str):
        """
        Сохраняет профиль пользователя в Redis и инвалидирует его кэш.

        :param user_id: Идентификатор пользователя.
        :param name: Имя пользователя.
        :param age: Возраст пользователя.
        :param city: Город пользователя.
        """
        self.repository.save_user_profile(user_id=user_id, name=name, age=age, city=city)
        self.cache.invalidate_cache(user_id=user_id)

    def track_unique_user(self, user_id: int):
        """
        Добавляет пользователя в множество уникальных пользователей.

        :param user_id: Идентификатор пользователя.
        """
        self.repository.track_unique_user(user_id=user_id)

    def update_user_activity(self, user_id: int):
        """
        Обновляет активность пользователя в Redis.

        :param user_id: Идентификатор пользователя.
        """
        self.repository.update_user_activity(user_id=user_id)

    def get_user_profile(self, user_id):
        """
        Получает профиль пользователя из Redis.

        :param user_id: Идентификатор пользователя.
        :return: Данные профиля пользователя.
        """
        return self.repository.get_user_profile(user_id=user_id)

    def increment_statistics_bulk(self, event_type: str, user_id: int):
        """
        Увеличивает статистику для нескольких событий.

        :param event_type: Тип события.
        :param user_id: Идентификатор пользователя.
        """
        events = [{
            "event_type": event_type,
            "user_id": user_id
        }]
        self.repository.increment_statistics_bulk(events=events)

    def increment_event_count(self, event_type: str):
        """
        Увеличивает счетчик для конкретного типа события.

        :param event_type: Тип события.
        """
        self.repository.increment_event_count(event_type=event_type)

    def get_event_count(self, event_type: str):
        """
        Получает количество событий для конкретного типа.

        :param event_type: Тип события.
        :return: Количество событий данного типа.
        """
        return self.repository.get_event_count(event_type=event_type)

    def increment_user_activity(self, user_id: int):
        """
        Увеличивает активность пользователя на 1.

        :param user_id: Идентификатор пользователя.
        """
        self.repository.increment_user_activity(user_id=user_id)

    def get_user_activity(self, user_id: int):
        """
        Получает уровень активности пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Уровень активности пользователя.
        """
        return self.repository.get_user_activity(user_id=user_id)

    def get_redis_stats(self):
        """
        Получает статистику Redis, такую как количество подключений, использованную память и другие параметры.

        :return: Статистика Redis.
        """
        return self.repository.get_redis_stats()

    """
    Redis Cache
    """

    def cache_user_profile(self, user_id: int, profile_data: dict, expire_time: int = 300):
        """
        Кэширует профиль пользователя в Redis с указанным временем жизни.

        :param user_id: Идентификатор пользователя.
        :param profile_data: Данные профиля пользователя в виде словаря.
        :param expire_time: Время жизни кэша в секундах (по умолчанию 300 секунд).
        """
        self.cache.cache_user_profile(user_id=user_id, profile_data=profile_data, expire_time=expire_time)

    def get_cache_user_profile(self, user_id: int) -> User:
        """
        Получает профиль пользователя из кэша Redis.

        :param user_id: Идентификатор пользователя.
        :return: Данные профиля пользователя из кэша.
        """
        cached_profile = self.cache.get_cache_user_profile(user_id=user_id)
        return cached_profile

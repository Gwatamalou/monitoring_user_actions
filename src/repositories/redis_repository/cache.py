import json
from .base import RedisRepositoryBase


class RedisCache(RedisRepositoryBase):
    """
    Класс для работы с кэшированием профилей пользователей в Redis.
    Наследуется от базового класса RedisRepositoryBase.
    """

    def cache_user_profile(self, user_id: int, profile_data: dict, expire_time: int = 300):
        """
        Сохраняет данные профиля пользователя в кэш с заданным временем жизни.

        :param user_id: Идентификатор пользователя.
        :param profile_data: Данные профиля пользователя в виде словаря.
        :param expire_time: Время жизни кэша в секундах (по умолчанию 300 секунд).
        """
        self.client.setex(f"user_cache:{user_id}", expire_time, json.dumps(profile_data))

    def get_cache_user_profile(self, user_id: int):
        """
        Получает данные профиля пользователя из кэша.

        :param user_id: Идентификатор пользователя.
        :return: Данные профиля в виде словаря, если данные существуют в кэше, иначе None.
        """
        data = self.client.get(f"user_cache:{user_id}")
        return json.loads(data) if data else None

    def invalidate_cache(self, user_id: int):
        """
        Удаляет кэшированные данные профиля пользователя.

        :param user_id: Идентификатор пользователя.
        """
        self.client.delete(f"user_cache:{user_id}")

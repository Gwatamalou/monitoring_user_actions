import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from .depends import get_redis_services
from .schemas import User, Event

app = FastAPI()

@app.get("/")
def read_root():
    """
    Корневой эндпоинт для проверки работы API.

    :return: Словарь с сообщением, подтверждающим работу API.
    """
    return {"message": "Event Processing API работает!"}

@app.post("/users/{user_id}")
def create_user(user_id: int,
                user: User,
                redis_services=Depends(get_redis_services)):
    """
    Создает новый профиль пользователя и сохраняет его в кэше Redis.

    :param user_id: Идентификатор пользователя.
    :param user: Данные пользователя (имя, возраст, город).
    :param redis_services: Сервис Redis для взаимодействия с кэшем.
    :return: None
    """
    redis_services.save_user_profile(user_id=user_id,
                                     name=user.name,
                                     age=user.age,
                                     city=user.city)

@app.get("/user/{user_id}")
def get_user(user_id: int,
             redis_services=Depends(get_redis_services)):
    """
    Получает профиль пользователя из кэша или Redis.

    :param user_id: Идентификатор пользователя.
    :param redis_services: Сервис Redis для взаимодействия с кэшем.
    :return: Словарь с данными пользователя и источником данных.
    :raise HTTPException: Если профиль пользователя не найден, генерируется ошибка 404.
    """
    cached_profile = redis_services.get_cache_user_profile(user_id)
    print(f"CACHE {cached_profile}")
    if cached_profile:
        return {"source": "cache", "data": cached_profile}

    user_data = redis_services.get_user_profile(user_id)
    print(f"USER_DATA {user_data}")
    if user_data:
        return {"source": "set", "data": user_data}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Пользователь не найден")

@app.post("/events")
def send_event(event: Event,
               redis_services=Depends(get_redis_services)):
    """
    Логирует событие в очередь Redis и обновляет статистику по событиям.

    :param event: Данные о событии (пользователь, тип события, метаданные).
    :param redis_services: Сервис Redis для взаимодействия с кэшем.
    :return: Сообщение, подтверждающее добавление события в очередь.
    """
    redis_services.log_event(user_id=event.user_id,
                             event_type=event.event_type,
                             metadata=event.metadata)
    redis_services.increment_event_count(event_type=event.event_type)
    redis_services.increment_user_activity(user_id=event.user_id)

    return {"message": "Событие добавлено в очередь"}

@app.get("/statistics/events/{event_type}")
def get_event_statistics(event_type: str,
                         redis_services=Depends(get_redis_services)):
    """
    Получает статистику по конкретному типу события.

    :param event_type: Тип события для получения статистики.
    :param redis_services: Сервис Redis для взаимодействия с кэшем.
    :return: Словарь с типом события и количеством.
    :raise HTTPException: Если статистика по событию не найдена, генерируется ошибка 404.
    """
    count = redis_services.get_event_count(event_type=event_type)
    if count:
        return {"event_type": event_type, "count": count}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Тип события не найден: {event_type}")

@app.get("/statistics/user/{user_id}")
def get_user_statistics(user_id: int,
                        redis_services=Depends(get_redis_services)):
    """
    Получает статистику активности конкретного пользователя.

    :param user_id: Идентификатор пользователя для получения статистики.
    :param redis_services: Сервис Redis для взаимодействия с кэшем.
    :return: Словарь с идентификатором пользователя и его активностью.
    :raise HTTPException: Если статистика активности пользователя не найдена, генерируется ошибка 404.
    """
    count = redis_services.get_user_activity(user_id=user_id)
    if count:
        return {"user_id": user_id, "activity_score": count}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Активность для пользователя не найдена: {user_id}")

@app.get("/monitoring")
def get_monitoring_data(redis_services=Depends(get_redis_services)):
    """
    Получает данные мониторинга для Redis.

    :param redis_services: Сервис Redis для получения статистики.
    :return: Словарь с данными мониторинга Redis.
    """
    return redis_services.get_redis_stats()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

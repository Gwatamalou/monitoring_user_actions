import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from depends import get_redis_services
from schemas import User, Event

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Event Processing API работает!"}


@app.post("/users/{user_id}")
def create_user(user_id: int,
                user: User,
                redis_services=Depends(get_redis_services)):
    redis_services.save_user_profile(user_id=user_id,
                                     name=user.name,
                                     age=user.age,
                                     city=user.city)


@app.get("/user/{user_id}")
def get_suer(user_id: int,
             redis_services=Depends(get_redis_services)):
    cached_profile = redis_services.get_cache_user_profile(user_id)
    print(f"CACHE {cached_profile}")
    if cached_profile:
        return {"source": "cache", "data": cached_profile}

    user_data = redis_services.get_user_profile(user_id)
    print(f"USER_DATA {user_data}")
    if user_data:
        return {"source": "set", "data": user_data}

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="user bot found")


@app.post("/events")
def send_event(event: Event,
               redis_services=Depends(get_redis_services)):
    redis_services.log_event(user_id=event.user_id,
                             event_type=event.event_type,
                             metadata=event.metadata)
    redis_services.increment_event_count(event_type=event.event_type)
    redis_services.increment_user_activity(user_id=event.user_id)

    return {"message": "Событие добавлено в очередь"}

@app.get("/statistics/events/{event_type}")
def get_event_statistics(event_type: str,
                         redis_services=Depends(get_redis_services)):
    count = redis_services.get_event_count(event_type=event_type)
    if count:
        return {"event_type": event_type, "count": count}

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"not fount event_type: {event_type}")

@app.get("/statistics/user/{user_id}")
def get_user_statistics(user_id: int,
                        redis_services=Depends(get_redis_services)):
    count = redis_services.get_user_activity(user_id=user_id)
    if count:
        return {"user_id": user_id, "activity_score": count}

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Not found activity user: {user_id}")

@app.get("/monitoring")
def get_monitoring_data(redis_services=Depends(get_redis_services)):
    return redis_services.get_redis_stats()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

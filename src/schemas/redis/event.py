from pydantic import BaseModel




class Event(BaseModel):
    user_id: int
    event_type: str
    metadata: dict



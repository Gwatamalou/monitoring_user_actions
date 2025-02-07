from pydantic import BaseModel, Field
from typing import Annotated



class User(BaseModel):
    name: Annotated[str, Field(max_length=30)]
    age: int
    city: Annotated[str, Field(max_length=50)]

class UserIn(User):
    user_id: int

class UserOut(User):
    user_id: int

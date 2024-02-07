from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    surname: str
    firstname: str
    is_active: bool = False
    time_created: datetime

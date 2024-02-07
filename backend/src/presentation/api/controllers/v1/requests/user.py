from pydantic import BaseModel, EmailStr


class UserInSchema(BaseModel):
    password: str
    username: str
    email: EmailStr
    surname: str
    firstname: str

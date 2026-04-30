from pydantic import BaseModel, EmailStr


class Request(BaseModel):
    email: EmailStr
    password: str
    group: str

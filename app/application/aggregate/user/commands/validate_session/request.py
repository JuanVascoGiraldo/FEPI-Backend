from pydantic import BaseModel, EmailStr


class Request(BaseModel):
    token: str

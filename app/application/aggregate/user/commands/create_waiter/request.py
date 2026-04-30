from typing import Optional
from pydantic import BaseModel, EmailStr


class Request(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    group: str
    phone: Optional[str] = None

from typing import Optional
from pydantic import BaseModel, EmailStr

SUPERADMIN_GROUP = "Admin"


class Request(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

from typing import Optional
from pydantic import BaseModel, EmailStr


class Request(BaseModel):
    email: EmailStr
    group: Optional[str] = None

from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class Request(BaseModel):
    email: EmailStr
    group: Optional[str] = None
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("New password must be at least 8 characters")
        return v

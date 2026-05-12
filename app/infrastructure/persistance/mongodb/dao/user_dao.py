from __future__ import annotations

from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import EmailStr

from .base_dao import BaseDao


USER_PK_INDEX = "USER#"
USER_SK_INDEX = "PROFILE#"


class UserDao(BaseDao):
    PK: ClassVar[str] = USER_PK_INDEX
    SK: ClassVar[str] = USER_SK_INDEX
    # email, group and role are excluded — they are used in MongoDB query filters.
    ENCRYPTED_FIELDS: ClassVar[frozenset[str]] = frozenset({"first_name", "last_name", "phone"})

    id: UUID
    group: str | None = None
    first_name: str
    last_name: str
    email: EmailStr
    password_hash: str
    role: int
    is_active: bool
    phone: str | None = None
    created_at: datetime
    updated_at: datetime

    def build_pk(self) -> str:
        return f"{self.PK}{self.id}"

    def build_sk(self) -> str:
        return self.SK

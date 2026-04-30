from __future__ import annotations

from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import Field

from .base_dao import BaseDao


SESSION_PK_INDEX = "SESSION#"
SESSION_SK_INDEX = "DATA#"


class SessionDao(BaseDao):
    PK: ClassVar[str] = SESSION_PK_INDEX
    SK: ClassVar[str] = SESSION_SK_INDEX

    id: UUID
    token: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    expiration_date: datetime
    extra_fields: dict = Field(default_factory=dict)

    def build_pk(self) -> str:
        return f"{self.PK}{self.id}"

    def build_sk(self) -> str:
        return self.SK

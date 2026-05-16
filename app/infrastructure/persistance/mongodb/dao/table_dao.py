from __future__ import annotations

from datetime import datetime
from typing import ClassVar
from uuid import UUID

from .base_dao import BaseDao


TABLE_PK_INDEX = "TABLE#"
TABLE_SK_INDEX = "INFO#"


class TableDao(BaseDao):
    PK: ClassVar[str] = TABLE_PK_INDEX
    SK: ClassVar[str] = TABLE_SK_INDEX
    # group, status and number are excluded — they are used in MongoDB query filters.
    ENCRYPTED_FIELDS: ClassVar[frozenset[str]] = frozenset({"description"})

    id: UUID
    group: str
    number: str
    description: str | None = None
    status: int
    created_at: datetime
    updated_at: datetime

    def build_pk(self) -> str:
        return f"{self.PK}{self.id}"

    def build_sk(self) -> str:
        return self.SK

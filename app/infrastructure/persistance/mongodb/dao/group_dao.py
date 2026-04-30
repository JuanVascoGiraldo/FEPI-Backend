from __future__ import annotations

from datetime import datetime
from typing import ClassVar
from uuid import UUID

from .base_dao import BaseDao

GROUP_PK_INDEX = "GROUP#"
GROUP_SK_INDEX = "INFO#"


class GroupDao(BaseDao):
    PK: ClassVar[str] = GROUP_PK_INDEX
    SK: ClassVar[str] = GROUP_SK_INDEX

    id: UUID
    name: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    def build_pk(self) -> str:
        return f"{self.PK}{self.id}"

    def build_sk(self) -> str:
        return self.SK

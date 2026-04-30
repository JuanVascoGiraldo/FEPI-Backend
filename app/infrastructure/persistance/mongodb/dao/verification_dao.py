from __future__ import annotations

from datetime import datetime
from typing import ClassVar
from uuid import UUID

from .base_dao import BaseDao


VERIFICATION_PK_INDEX = "VERIFICATION#"
VERIFICATION_SK_INDEX = "DATA#"


class VerificationDao(BaseDao):
    PK: ClassVar[str] = VERIFICATION_PK_INDEX
    SK: ClassVar[str] = VERIFICATION_SK_INDEX

    id: UUID
    value_id: str
    type: int
    code: str
    is_valid: bool = False
    created_at: datetime
    updated_at: datetime
    expiration_date: datetime

    def build_pk(self) -> str:
        return f"{self.PK}{self.id}"

    def build_sk(self) -> str:
        return self.SK

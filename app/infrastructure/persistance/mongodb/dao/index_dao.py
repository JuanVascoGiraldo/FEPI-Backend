from __future__ import annotations

from .base_dao import BaseDao


class IndexDao(BaseDao):
    """Generic DAO for records that only store PK and SK."""

    pk: str
    sk: str

    def build_pk(self) -> str:
        return self.pk

    def build_sk(self) -> str:
        return self.sk

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict


class BaseDao(BaseModel):
    """Base DAO model with PK/SK prefixes and document mapping helpers."""

    model_config = ConfigDict(extra="ignore")

    PK: ClassVar[str] = ""
    SK: ClassVar[str] = ""

    def build_pk(self) -> str:
        raise NotImplementedError("Child DAO must implement build_pk")

    def build_sk(self) -> str:
        raise NotImplementedError("Child DAO must implement build_sk")

    def to_document(self) -> dict[str, Any]:
        data = self.model_dump(mode="json")
        data["pk"] = self.build_pk()
        data["sk"] = self.build_sk()
        return data

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BaseDao:
        data = dict(document)
        data.pop("pk", None)
        data.pop("sk", None)
        return cls.model_validate(data)

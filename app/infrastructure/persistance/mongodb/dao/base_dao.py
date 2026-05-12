from __future__ import annotations

from typing import Any, Callable, ClassVar

from pydantic import BaseModel, ConfigDict


class BaseDao(BaseModel):
    """Base DAO model with PK/SK prefixes and document mapping helpers."""

    model_config = ConfigDict(extra="ignore")

    PK: ClassVar[str] = ""
    SK: ClassVar[str] = ""

    # Subclasses declare which fields are symmetrically encrypted at rest.
    # Only fields that are NOT used as MongoDB query filters should be listed here.
    ENCRYPTED_FIELDS: ClassVar[frozenset[str]] = frozenset()

    def build_pk(self) -> str:
        raise NotImplementedError("Child DAO must implement build_pk")

    def build_sk(self) -> str:
        raise NotImplementedError("Child DAO must implement build_sk")

    def to_document(self) -> dict[str, Any]:
        data = self.model_dump(mode="json")
        data["pk"] = self.build_pk()
        data["sk"] = self.build_sk()
        return data

    def to_encrypted_document(self, encrypt: Callable[[str], str]) -> dict[str, Any]:
        """Serialize to a document and encrypt all ENCRYPTED_FIELDS before storage."""
        data = self.to_document()
        for field in self.ENCRYPTED_FIELDS:
            value = data.get(field)
            if value is not None:
                data[field] = encrypt(str(value))
        return data

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BaseDao:
        data = dict(document)
        data.pop("pk", None)
        data.pop("sk", None)
        return cls.model_validate(data)

    @classmethod
    def from_encrypted_document(
        cls, document: dict[str, Any], decrypt: Callable[[str], str]
    ) -> BaseDao:
        """Decrypt ENCRYPTED_FIELDS from a raw document, then deserialize."""
        data = dict(document)
        for field in cls.ENCRYPTED_FIELDS:
            value = data.get(field)
            if value is not None:
                data[field] = decrypt(str(value))
        return cls.from_document(data)

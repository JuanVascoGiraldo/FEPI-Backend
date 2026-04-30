from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MongoClient(ABC):
    """Abstract Mongo client with basic CRUD operations."""

    @abstractmethod
    async def insert_one(self, collection: str, document: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_one(
        self,
        collection: str,
        filters: dict[str, Any],
    ) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def find_many(
        self,
        collection: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(
        self,
        collection: str,
        filters: dict[str, Any],
        update_fields: dict[str, Any],
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, collection: str, filters: dict[str, Any]) -> bool:
        raise NotImplementedError

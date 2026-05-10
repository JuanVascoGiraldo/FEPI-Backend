from __future__ import annotations

from copy import deepcopy
from typing import Any

from .mongo_client import MongoClient


class MongoTestClient(MongoClient):
    """In-memory Mongo client for tests using Python dictionaries."""

    def __init__(self) -> None:
        self._store: dict[str, list[dict[str, Any]]] = {}

    def _collection(self, collection: str) -> list[dict[str, Any]]:
        if collection not in self._store:
            self._store[collection] = []
        return self._store[collection]

    @staticmethod
    def _matches(document: dict[str, Any], filters: dict[str, Any]) -> bool:
        for key, value in filters.items():
            if document.get(key) != value:
                return False
        return True

    async def insert_one(self, collection: str, document: dict[str, Any]) -> None:
        self._collection(collection).append(deepcopy(document))

    async def find_one(
        self,
        collection: str,
        filters: dict[str, Any],
    ) -> dict[str, Any] | None:
        for item in self._collection(collection):
            if self._matches(item, filters):
                return deepcopy(item)
        return None

    async def find_many(
        self,
        collection: str,
        filters: dict[str, Any],
        projection: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        results = [
            deepcopy(item)
            for item in self._collection(collection)
            if self._matches(item, filters)
        ]
        if projection is None:
            return results
        include_keys = {k for k, v in projection.items() if v == 1}
        exclude_keys = {k for k, v in projection.items() if v == 0}
        projected = []
        for item in results:
            if include_keys:
                projected.append({k: v for k, v in item.items() if k in include_keys})
            else:
                projected.append({k: v for k, v in item.items() if k not in exclude_keys})
        return projected

    async def update_one(
        self,
        collection: str,
        filters: dict[str, Any],
        update_fields: dict[str, Any],
    ) -> bool:
        items = self._collection(collection)
        for item in items:
            if self._matches(item, filters):
                item.update(deepcopy(update_fields))
                return True
        return False

    async def delete_one(self, collection: str, filters: dict[str, Any]) -> bool:
        items = self._collection(collection)
        for index, item in enumerate(items):
            if self._matches(item, filters):
                del items[index]
                return True
        return False

    async def ensure_indexes(self) -> None:
        pass

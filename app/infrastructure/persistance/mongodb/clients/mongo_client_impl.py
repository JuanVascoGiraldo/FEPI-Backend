from __future__ import annotations

from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.config import Config

from .mongo_client import MongoClient


class MongoClientImpl(MongoClient):
    """Production Mongo implementation backed by Motor."""

    def __init__(self, config: Config) -> None:
        mongo_url = getattr(config, "mongodb_url", "mongodb://localhost:27017")
        mongo_db = getattr(config, "mongodb_db", "fepi")
        self._client = AsyncIOMotorClient(
            mongo_url,
            uuidRepresentation="standard",
        )
        self._db = self._client[mongo_db]

    def _get_collection(self, collection: str) -> AsyncIOMotorCollection:
        return self._db[collection]

    async def insert_one(self, collection: str, document: dict[str, Any]) -> None:
        await self._get_collection(collection).insert_one(document)

    async def find_one(
        self,
        collection: str,
        filters: dict[str, Any],
    ) -> dict[str, Any] | None:
        return await self._get_collection(collection).find_one(filters)

    async def find_many(
        self,
        collection: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        cursor = self._get_collection(collection).find(filters)
        return await cursor.to_list(length=None)

    async def update_one(
        self,
        collection: str,
        filters: dict[str, Any],
        update_fields: dict[str, Any],
    ) -> bool:
        result = await self._get_collection(collection).update_one(
            filters,
            {"$set": update_fields},
        )
        return result.modified_count > 0

    async def delete_one(self, collection: str, filters: dict[str, Any]) -> bool:
        result = await self._get_collection(collection).delete_one(filters)
        return result.deleted_count > 0

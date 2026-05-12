from __future__ import annotations

from typing import Any

import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import ASCENDING

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
            tls=True,
            tlsCAFile=certifi.where(),
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
        projection: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        cursor = self._get_collection(collection).find(filters, projection)
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

    async def ensure_indexes(self) -> None:
        users = self._get_collection("users")
        await users.create_index([("pk", ASCENDING), ("sk", ASCENDING)], unique=True, background=True)
        await users.create_index([("sk", ASCENDING), ("role", ASCENDING)], background=True)
        await users.create_index([("sk", ASCENDING), ("group", ASCENDING)], background=True)
        await users.create_index([("sk", ASCENDING), ("group", ASCENDING), ("role", ASCENDING)], background=True)
        await users.create_index([("sk", ASCENDING), ("email", ASCENDING)], background=True)

        dishes = self._get_collection("dishes")
        await dishes.create_index([("pk", ASCENDING), ("sk", ASCENDING)], unique=True, background=True)
        await dishes.create_index([("sk", ASCENDING), ("group", ASCENDING)], background=True)

        tables = self._get_collection("tables")
        await tables.create_index([("pk", ASCENDING), ("sk", ASCENDING)], unique=True, background=True)
        await tables.create_index([("sk", ASCENDING), ("group", ASCENDING)], background=True)

        orders = self._get_collection("orders")
        await orders.create_index([("pk", ASCENDING), ("sk", ASCENDING)], unique=True, background=True)
        await orders.create_index([("sk", ASCENDING), ("group", ASCENDING)], background=True)

        indexes = self._get_collection("indexes")
        await indexes.create_index([("pk", ASCENDING)], unique=True, background=True)

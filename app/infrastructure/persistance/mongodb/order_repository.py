from typing import Any, Callable, List, Optional
from uuid import UUID

from app.config import Config
from app.domain.aggregate.order import Order, OrderStatus
from app.domain.repositories.order_repository import OrderRepository
from app.domain.services.encryption_service import EncryptionService
from app.infrastructure.persistance.mongodb.clients import MongoClient
from app.infrastructure.persistance.mongodb.dao.order_dao import OrderDao
from app.infrastructure.persistance.mongodb.dao.index_dao import IndexDao
from app.infrastructure.persistance.mongodb.dao.payment_dao import PaymentDao
from app.infrastructure.persistance.mongodb.mappers.order import from_dao_to_order, from_order_to_dao

TABLE_PK_PREFIX = "TABLE#"
ORDER_SK_PREFIX = "ORDER#"


def _encrypt_payments(payments: list[dict], encrypt: Callable[[str], str]) -> list[dict]:
    result = []
    for p in payments:
        encrypted = dict(p)
        for field in PaymentDao.ENCRYPTED_FIELDS:
            if encrypted.get(field) is not None:
                encrypted[field] = encrypt(str(encrypted[field]))
        result.append(encrypted)
    return result


def _decrypt_payments(payments: list[dict], decrypt: Callable[[str], str]) -> list[dict]:
    result = []
    for p in payments:
        decrypted = dict(p)
        for field in PaymentDao.ENCRYPTED_FIELDS:
            if decrypted.get(field) is not None:
                decrypted[field] = decrypt(str(decrypted[field]))
        result.append(decrypted)
    return result


class OrderRepositoryImpl(OrderRepository):
    COLLECTION = "orders"
    INDEX_COLLECTION = "indexes"

    def __init__(
        self,
        mongo_client: MongoClient,
        config: Config,
        encryption_service: EncryptionService,
    ) -> None:
        self.mongo_client = mongo_client
        self.config = config
        self._encrypt = encryption_service.encrypt
        self._decrypt = encryption_service.decrypt

    def _to_doc(self, dao: OrderDao) -> dict[str, Any]:
        document = dao.to_encrypted_document(self._encrypt)
        document["payments"] = _encrypt_payments(document.get("payments", []), self._encrypt)
        return document

    def _from_doc(self, document: dict[str, Any]) -> OrderDao:
        data = dict(document)
        data["payments"] = _decrypt_payments(data.get("payments", []), self._decrypt)
        return OrderDao.from_encrypted_document(data, self._decrypt)

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"pk": f"{OrderDao.PK}{order_id}", "sk": OrderDao.SK},
        )
        if document is None:
            return None
        return from_dao_to_order(self._from_doc(document))

    async def get_by_group(self, group: str) -> List[Order]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": OrderDao.SK, "group": group},
        )
        return [from_dao_to_order(self._from_doc(d)) for d in documents]

    async def get_ids_by_group(self, group: str) -> List[UUID]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": OrderDao.SK, "group": group},
            {"id": 1, "_id": 0},
        )
        return [UUID(str(d["id"])) for d in documents]

    async def get_by_table_id(self, table_id: UUID) -> List[Order]:
        index_docs = await self.mongo_client.find_many(
            self.INDEX_COLLECTION,
            {"pk": f"{TABLE_PK_PREFIX}{table_id}"},
        )
        orders = []
        for idx in index_docs:
            order_id = UUID(idx["sk"].replace(ORDER_SK_PREFIX, "", 1))
            order = await self.get_by_id(order_id)
            if order:
                orders.append(order)
        return orders

    async def get_open_by_table(self, table_id: UUID) -> Optional[Order]:
        open_statuses = [int(OrderStatus.OPEN), int(OrderStatus.IN_PROCESS), int(OrderStatus.PAYING)]
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"sk": OrderDao.SK, "table_id": str(table_id), "status": {"$in": open_statuses}},
        )
        if document is None:
            return None
        return from_dao_to_order(self._from_doc(document))

    async def get_by_group_and_status(self, group: str, status: OrderStatus) -> List[Order]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": OrderDao.SK, "group": group, "status": int(status)},
        )
        return [from_dao_to_order(self._from_doc(d)) for d in documents]

    async def create(self, order: Order) -> None:
        dao = from_order_to_dao(order)
        document = self._to_doc(dao)
        document["entity"] = "ORDER"
        await self.mongo_client.insert_one(self.COLLECTION, document)

        table_index = IndexDao(
            pk=f"{TABLE_PK_PREFIX}{order.table_id}",
            sk=f"{ORDER_SK_PREFIX}{order.id}",
        )
        index_doc = table_index.to_document()
        index_doc["entity"] = "ORDER_TABLE_INDEX"
        await self.mongo_client.insert_one(self.INDEX_COLLECTION, index_doc)

    async def update(self, order: Order) -> None:
        dao = from_order_to_dao(order)
        document = self._to_doc(dao)
        update_fields = {k: v for k, v in document.items() if k not in ("pk", "sk")}
        await self.mongo_client.update_one(
            self.COLLECTION,
            {"pk": f"{OrderDao.PK}{order.id}", "sk": OrderDao.SK},
            update_fields,
        )

    async def delete(self, order_id: UUID) -> None:
        await self.mongo_client.delete_one(
            self.COLLECTION,
            {"pk": f"{OrderDao.PK}{order_id}", "sk": OrderDao.SK},
        )

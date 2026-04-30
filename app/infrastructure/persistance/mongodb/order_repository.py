from typing import List, Optional
from uuid import UUID

from app.config import Config
from app.domain.aggregate.order import Order, OrderStatus
from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.persistance.mongodb.clients import MongoClient
from app.infrastructure.persistance.mongodb.dao.order_dao import OrderDao
from app.infrastructure.persistance.mongodb.dao.index_dao import IndexDao
from app.infrastructure.persistance.mongodb.mappers.order import from_dao_to_order, from_order_to_dao

TABLE_PK_PREFIX = "TABLE#"
ORDER_SK_PREFIX = "ORDER#"


class OrderRepositoryImpl(OrderRepository):
    COLLECTION = "orders"
    INDEX_COLLECTION = "indexes"

    def __init__(self, mongo_client: MongoClient, config: Config) -> None:
        self.mongo_client = mongo_client
        self.config = config

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"pk": f"{OrderDao.PK}{order_id}", "sk": OrderDao.SK},
        )
        if document is None:
            return None
        return from_dao_to_order(OrderDao.from_document(document))

    async def get_by_group(self, group: str) -> List[Order]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": OrderDao.SK, "group": group},
        )
        return [from_dao_to_order(OrderDao.from_document(d)) for d in documents]

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
        return from_dao_to_order(OrderDao.from_document(document))

    async def get_by_group_and_status(self, group: str, status: OrderStatus) -> List[Order]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": OrderDao.SK, "group": group, "status": int(status)},
        )
        return [from_dao_to_order(OrderDao.from_document(d)) for d in documents]

    async def create(self, order: Order) -> None:
        dao = from_order_to_dao(order)
        document = dao.to_document()
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
        update_fields = dao.model_dump(mode="json", exclude={"pk", "sk"})
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

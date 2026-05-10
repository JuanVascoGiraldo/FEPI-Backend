from typing import List, Optional
from uuid import UUID

from app.config import Config
from app.domain.aggregate.dish import Dish, FoodCategory
from app.domain.aggregate.dish.dish_status_type import DishStatusType
from app.domain.repositories.dish_repository import DishRepository
from app.infrastructure.persistance.mongodb.clients import MongoClient
from app.infrastructure.persistance.mongodb.dao.dish_dao import DishDao
from app.infrastructure.persistance.mongodb.mappers.dish import from_dao_to_dish, from_dish_to_dao


class DishRepositoryImpl(DishRepository):
    COLLECTION = "dishes"

    def __init__(self, mongo_client: MongoClient, config: Config) -> None:
        self.mongo_client = mongo_client
        self.config = config

    async def get_by_id(self, dish_id: UUID) -> Optional[Dish]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"pk": f"{DishDao.PK}{dish_id}", "sk": DishDao.SK},
        )
        if document is None:
            return None
        return from_dao_to_dish(DishDao.from_document(document))

    async def get_by_group(self, group: str) -> List[Dish]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": DishDao.SK, "group": group},
        )
        return [from_dao_to_dish(DishDao.from_document(d)) for d in documents]

    async def get_ids_by_group(self, group: str) -> List[UUID]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": DishDao.SK, "group": group},
            {"id": 1, "_id": 0},
        )
        return [UUID(str(d["id"])) for d in documents]

    async def get_available_by_group(self, group: str) -> List[Dish]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": DishDao.SK, "group": group, "status_type": int(DishStatusType.AVAILABLE)},
        )
        return [from_dao_to_dish(DishDao.from_document(d)) for d in documents]

    async def get_by_group_and_category(self, group: str, category: FoodCategory) -> List[Dish]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": DishDao.SK, "group": group, "category": int(category)},
        )
        return [from_dao_to_dish(DishDao.from_document(d)) for d in documents]

    async def create(self, dish: Dish) -> None:
        dao = from_dish_to_dao(dish)
        document = dao.to_document()
        document["entity"] = "DISH"
        await self.mongo_client.insert_one(self.COLLECTION, document)

    async def update(self, dish: Dish) -> None:
        dao = from_dish_to_dao(dish)
        update_fields = dao.model_dump(mode="json", exclude={"pk", "sk"})
        await self.mongo_client.update_one(
            self.COLLECTION,
            {"pk": f"{DishDao.PK}{dish.id}", "sk": DishDao.SK},
            update_fields,
        )

    async def delete(self, dish_id: UUID) -> None:
        await self.mongo_client.delete_one(
            self.COLLECTION,
            {"pk": f"{DishDao.PK}{dish_id}", "sk": DishDao.SK},
        )

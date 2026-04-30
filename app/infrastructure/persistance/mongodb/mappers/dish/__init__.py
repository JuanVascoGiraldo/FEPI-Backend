from app.domain.aggregate.dish import Dish, DishStatus, DishStatusType, FoodCategory
from app.infrastructure.persistance.mongodb.dao.dish_dao import DishDao


def from_dish_to_dao(dish: Dish) -> DishDao:
    return DishDao(
        id=dish.id,
        group=dish.group,
        name=dish.name,
        description=dish.description,
        price=dish.price,
        category=int(dish.category),
        status_type=int(dish.status.type),
        status_description=dish.status.description,
        image_url=dish.image_url,
        created_at=dish.created_at,
        updated_at=dish.updated_at,
    )


def from_dao_to_dish(dao: DishDao) -> Dish:
    return Dish(
        id=dao.id,
        group=dao.group,
        name=dao.name,
        description=dao.description,
        price=dao.price,
        category=FoodCategory(dao.category),
        status=DishStatus(
            type=DishStatusType(dao.status_type),
            description=dao.status_description,
        ),
        image_url=dao.image_url,
        created_at=dao.created_at,
        updated_at=dao.updated_at,
    )

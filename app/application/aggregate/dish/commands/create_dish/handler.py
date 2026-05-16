from logging import Logger
from uuid import uuid4

from app.domain.aggregate.dish import Dish, FoodCategory, DishStatus, DishStatusType
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.repositories.dish_repository import DishRepository
from app.domain.exceptions import IsNotAuthorizedException
from app.domain.aggregate.user.user_role import UserRole

from .request import Request
from .response import Response


class Handler:
    def __init__(self, dish_repository: DishRepository, logger: Logger) -> None:
        self.dish_repository = dish_repository
        self.logger = logger

    async def handle(self, request: Request, session: Meta) -> Response:
        if session.role != UserRole.ADMIN:
            raise IsNotAuthorizedException()

        timestamp = session.timestamp
        dish = Dish(
            id=uuid4(),
            group=session.group,
            name=request.name,
            description=request.description,
            price=request.price,
            category=FoodCategory(request.category),
            status=DishStatus(type=DishStatusType.AVAILABLE, description=""),
            image_url=request.image_url,
            created_at=timestamp,
            updated_at=timestamp,
        )
        await self.dish_repository.create(dish)
        self.logger.info(f"Dish created: {dish.id} ({dish.name}) for group {dish.group}")

        return Response(
            id=dish.id,
            group=dish.group,
            name=dish.name,
            description=dish.description,
            price=dish.price,
            tax=dish.tax,
            total_price=dish.total_price,
            category=int(dish.category),
            status=int(dish.status.type),
            image_url=dish.image_url,
            created_at=dish.created_at,
            updated_at=dish.updated_at,
        )

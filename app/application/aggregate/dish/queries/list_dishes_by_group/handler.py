from logging import Logger

from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.user.user_role import UserRole
from app.domain.exceptions import IsNotAuthorizedException
from app.domain.repositories.dish_repository import DishRepository

from .response import DishResponse, Response


class Handler:
    def __init__(self, dish_repository: DishRepository, logger: Logger) -> None:
        self.dish_repository = dish_repository
        self.logger = logger

    async def handle(self, session: Meta) -> Response:
        if session.role not in (UserRole.ADMIN, UserRole.WAITER):
            raise IsNotAuthorizedException()

        dishes = await self.dish_repository.get_by_group(session.group)

        return Response(
            dishes=[
                DishResponse(
                    id=d.id,
                    name=d.name,
                    description=d.description,
                    price=d.price,
                    tax=d.tax,
                    total_price=d.total_price,
                    category=int(d.category),
                    status=int(d.status.type),
                    image_url=d.image_url,
                    created_at=d.created_at,
                    updated_at=d.updated_at,
                )
                for d in dishes
            ]
        )

from asyncio import gather as asyncio_gather
from decimal import Decimal
from logging import Logger
from uuid import UUID

from app.domain.exceptions import TableNotFoundException
from app.domain.repositories.table_repository import TableRepository
from app.domain.repositories.dish_repository import DishRepository
from app.domain.repositories.order_repository import OrderRepository

from .response import ActiveOrderPublicResponse, DishPublicResponse, OrderItemPublicResponse, Response


class Handler:
    def __init__(
        self,
        table_repository: TableRepository,
        dish_repository: DishRepository,
        order_repository: OrderRepository,
        logger: Logger,
    ) -> None:
        self.table_repository = table_repository
        self.dish_repository = dish_repository
        self.order_repository = order_repository
        self.logger = logger

    async def handle(self, table_id: UUID) -> Response:
        table = await self.table_repository.get_by_id(table_id)
        if not table:
            raise TableNotFoundException(str(table_id))

        dishes, active_order = await asyncio_gather(
            self.dish_repository.get_available_by_group(table.group),
            self.order_repository.get_open_by_table(table_id),
        )

        active_order_response = None
        if active_order:
            total_paid = sum(
                (p.amount for p in active_order.payments if p.status == "confirmed"),
                Decimal("0"),
            )
            total_pending = active_order.total() - total_paid
            has_pending_request = any(
                p.status == "pending" for p in active_order.payments
            )

            active_order_response = ActiveOrderPublicResponse(
                id=active_order.id,
                items=[
                    OrderItemPublicResponse(
                        id=i.id,
                        name=i.name,
                        unit_price=i.unit_price,
                        quantity=i.quantity,
                        specifications=i.specifications,
                        status=int(i.status),
                    )
                    for i in active_order.items
                ],
                total=active_order.total(),
                total_paid=total_paid,
                total_pending=total_pending,
                has_pending_request=has_pending_request,
                created_at=active_order.created_at,
            )

        return Response(
            table_id=table.id,
            table_number=table.number,
            table_description=table.description,
            group=table.group,
            dishes=[
                DishPublicResponse(
                    id=d.id,
                    name=d.name,
                    description=d.description,
                    price=d.price,
                    tax=d.tax,
                    total_price=d.total_price,
                    category=int(d.category),
                    image_url=d.image_url,
                )
                for d in dishes
            ],
            active_order=active_order_response,
        )

from logging import Logger
from uuid import uuid4

from app.domain.aggregate.order.order_item import OrderItem
from app.domain.aggregate.order.order_item_status import OrderItemStatus
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.user.user_role import UserRole
from app.domain.exceptions import (
    IsNotAuthorizedException,
    OrderNotFoundException,
    DishNotFoundException,
)
from app.domain.repositories.order_repository import OrderRepository
from app.domain.repositories.dish_repository import DishRepository
from app.domain.repositories.table_repository import TableRepository
from app.infrastructure.events.event_bus import EventBus, Event

from .request import Request
from .response import OrderItemResponse, PaymentResponse, Response


class Handler:
    def __init__(
        self,
        order_repository: OrderRepository,
        dish_repository: DishRepository,
        table_repository: TableRepository,
        event_bus: EventBus,
        logger: Logger,
    ) -> None:
        self.order_repository = order_repository
        self.dish_repository = dish_repository
        self.table_repository = table_repository
        self.event_bus = event_bus
        self.logger = logger

    async def handle(self, order_id, request: Request, session: Meta) -> Response:
        if session.role not in (UserRole.ADMIN, UserRole.WAITER):
            raise IsNotAuthorizedException()

        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(str(order_id))

        dish = await self.dish_repository.get_by_id(request.dish_id)
        if not dish:
            raise DishNotFoundException(str(request.dish_id))

        item = OrderItem(
            id=uuid4(),
            dish_id=dish.id,
            name=dish.name,
            unit_price=dish.price,
            quantity=request.quantity,
            specifications=request.specifications,
            status=OrderItemStatus.PENDING,
        )
        order.add_item(item, session.timestamp)
        await self.order_repository.update(order)
        self.logger.info(f"Item {dish.name} x{request.quantity} added to order {order.id}")

        table = await self.table_repository.get_by_id(order.table_id)
        table_number = table.number if table else "?"

        await self.event_bus.publish(session.group, Event(
            type="order.item_added",
            payload={
                "table_id": str(order.table_id),
                "table_number": table_number,
                "order_id": str(order.id),
                "item_name": dish.name,
                "quantity": request.quantity,
                "order_total": str(order.total()),
            },
        ))

        return Response(
            id=order.id,
            group=order.group,
            table_id=order.table_id,
            waiter_id=order.waiter_id,
            items=[
                OrderItemResponse(
                    id=i.id,
                    dish_id=i.dish_id,
                    name=i.name,
                    unit_price=i.unit_price,
                    quantity=i.quantity,
                    specifications=i.specifications,
                    status=int(i.status),
                )
                for i in order.items
            ],
            payments=[
                PaymentResponse(
                    id=p.id,
                    amount=p.amount,
                    tip=p.tip,
                    email=p.email,
                    dish_ids=p.dish_ids,
                    created_at=p.created_at,
                )
                for p in order.payments
            ],
            status=int(order.status),
            notes=order.notes,
            total=order.total(),
            total_paid=order.total_paid(),
            total_pending=order.total_pending(),
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

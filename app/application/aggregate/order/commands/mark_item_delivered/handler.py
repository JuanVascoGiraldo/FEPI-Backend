from logging import Logger
from uuid import UUID

from app.domain.aggregate.order.order_item_status import OrderItemStatus
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.user.user_role import UserRole
from app.domain.exceptions import (
    IsNotAuthorizedException,
    OrderNotFoundException,
    OrderItemNotFoundException,
)
from app.domain.repositories.order_repository import OrderRepository
from app.domain.repositories.table_repository import TableRepository
from app.infrastructure.events.event_bus import EventBus, Event

from .response import OrderItemResponse, PaymentResponse, Response


class Handler:
    def __init__(
        self,
        order_repository: OrderRepository,
        table_repository: TableRepository,
        event_bus: EventBus,
        logger: Logger,
    ) -> None:
        self.order_repository = order_repository
        self.table_repository = table_repository
        self.event_bus = event_bus
        self.logger = logger

    async def handle(self, order_id: UUID, item_id: UUID, session: Meta) -> Response:
        if session.role not in (UserRole.ADMIN, UserRole.WAITER):
            raise IsNotAuthorizedException()

        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(str(order_id))

        item = order.get_item(item_id)
        if not item:
            raise OrderItemNotFoundException(str(item_id))

        item.status = OrderItemStatus.DELIVERED
        order.updated_at = session.timestamp
        await self.order_repository.update(order)

        self.logger.info("Item %s marked as DELIVERED in order %s", item_id, order_id)

        table = await self.table_repository.get_by_id(order.table_id)
        table_number = table.number if table else "?"

        await self.event_bus.publish(
            session.group,
            Event(
                type="order.item_delivered",
                payload={
                    "table_id": str(order.table_id),
                    "table_number": table_number,
                    "order_id": str(order_id),
                    "item_name": item.name,
                },
            ),
        )

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

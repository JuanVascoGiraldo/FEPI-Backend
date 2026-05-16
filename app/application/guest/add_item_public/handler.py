from logging import Logger
from uuid import UUID, uuid4

from app.domain.aggregate.order import Order, OrderStatus
from app.domain.aggregate.order.order_item import OrderItem
from app.domain.aggregate.order.order_item_status import OrderItemStatus
from app.domain.exceptions import TableNotFoundException, DishNotFoundException
from app.domain.repositories.table_repository import TableRepository
from app.domain.repositories.dish_repository import DishRepository
from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.events.event_bus import EventBus, Event

from .request import Request
from .response import OrderItemPublicResponse, Response


class Handler:
    def __init__(
        self,
        table_repository: TableRepository,
        dish_repository: DishRepository,
        order_repository: OrderRepository,
        event_bus: EventBus,
        logger: Logger,
    ) -> None:
        self.table_repository = table_repository
        self.dish_repository = dish_repository
        self.order_repository = order_repository
        self.event_bus = event_bus
        self.logger = logger

    async def handle(self, table_id: UUID, request: Request) -> Response:
        from datetime import datetime, timezone

        table = await self.table_repository.get_by_id(table_id)
        if not table:
            raise TableNotFoundException(str(table_id))

        dish = await self.dish_repository.get_by_id(request.dish_id)
        if not dish:
            raise DishNotFoundException(str(request.dish_id))

        timestamp = datetime.now(timezone.utc)

        order = await self.order_repository.get_open_by_table(table_id)
        if not order:
            order = Order(
                id=uuid4(),
                group=table.group,
                table_id=table_id,
                status=OrderStatus.OPEN,
                created_at=timestamp,
                updated_at=timestamp,
            )
            await self.order_repository.create(order)

        item = OrderItem(
            id=uuid4(),
            dish_id=dish.id,
            name=dish.name,
            unit_price=dish.price,
            quantity=request.quantity,
            specifications=request.specifications,
            status=OrderItemStatus.PENDING,
        )
        order.add_item(item, timestamp)
        await self.order_repository.update(order)
        self.logger.info(f"[public] Item {dish.name} x{request.quantity} added to order {order.id}")

        await self.event_bus.publish(table.group, Event(
            type="order.item_added",
            payload={
                "table_id": str(table_id),
                "table_number": table.number,
                "order_id": str(order.id),
                "item_name": dish.name,
                "quantity": request.quantity,
                "order_total": str(order.total()),
                "source": "customer",
            },
        ))

        return Response(
            order_id=order.id,
            items=[
                OrderItemPublicResponse(
                    id=i.id,
                    name=i.name,
                    unit_price=i.unit_price,
                    quantity=i.quantity,
                    specifications=i.specifications,
                    status=int(i.status),
                )
                for i in order.items
            ],
            total=order.total(),
            created_at=order.created_at,
        )

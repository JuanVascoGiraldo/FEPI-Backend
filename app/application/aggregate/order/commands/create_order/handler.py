from logging import Logger
from uuid import uuid4

from app.domain.aggregate.order import Order, OrderStatus
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.user.user_role import UserRole
from app.domain.exceptions import IsNotAuthorizedException, OrderAlreadyActiveException, TableNotFoundException
from app.domain.repositories.order_repository import OrderRepository
from app.domain.repositories.table_repository import TableRepository
from app.infrastructure.events.event_bus import EventBus, Event

from .request import Request
from .response import Response


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

    async def handle(self, request: Request, session: Meta) -> Response:
        if session.role not in (UserRole.ADMIN, UserRole.WAITER):
            raise IsNotAuthorizedException()

        table = await self.table_repository.get_by_id(request.table_id)
        if not table:
            raise TableNotFoundException(str(request.table_id))

        existing = await self.order_repository.get_open_by_table(request.table_id)
        if existing:
            raise OrderAlreadyActiveException(str(request.table_id))

        timestamp = session.timestamp
        waiter_id = session.user_id if session.role == UserRole.WAITER else None

        order = Order(
            id=uuid4(),
            group=session.group,
            table_id=request.table_id,
            waiter_id=waiter_id,
            notes=request.notes,
            status=OrderStatus.OPEN,
            created_at=timestamp,
            updated_at=timestamp,
        )
        await self.order_repository.create(order)
        self.logger.info(f"Order created: {order.id} for table {order.table_id}")

        await self.event_bus.publish(session.group, Event(
            type="order.created",
            payload={
                "table_id": str(table.id),
                "table_number": table.number,
                "order_id": str(order.id),
            },
        ))

        return Response(
            id=order.id,
            group=order.group,
            table_id=order.table_id,
            waiter_id=order.waiter_id,
            items=[],
            payments=[],
            status=int(order.status),
            notes=order.notes,
            total=order.total(),
            total_paid=order.total_paid(),
            total_pending=order.total_pending(),
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

from datetime import datetime, timezone
from decimal import Decimal
from logging import Logger
from uuid import UUID, uuid4

from app.domain.aggregate.order import OrderStatus
from app.domain.aggregate.order.payment import Payment
from app.domain.exceptions import TableNotFoundException, OrderNotFoundException
from app.domain.repositories.table_repository import TableRepository
from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.events.event_bus import EventBus, Event

from .request import Request
from .response import Response


class Handler:
    def __init__(
        self,
        table_repository: TableRepository,
        order_repository: OrderRepository,
        event_bus: EventBus,
        logger: Logger,
    ) -> None:
        self.table_repository = table_repository
        self.order_repository = order_repository
        self.event_bus = event_bus
        self.logger = logger

    async def handle(self, table_id: UUID, request: Request) -> Response:
        timestamp = datetime.now(timezone.utc)

        table = await self.table_repository.get_by_id(table_id)
        if not table:
            raise TableNotFoundException(str(table_id))

        order = await self.order_repository.get_open_by_table(table_id)
        if not order:
            raise OrderNotFoundException(str(table_id))

        if request.payment_type == "items" and request.item_ids:
            item_set = set(request.item_ids)
            amount = sum(
                (i.subtotal() for i in order.items if i.id in item_set),
                Decimal("0"),
            )
        else:
            amount = request.amount or Decimal("0")

        payment = Payment(
            id=uuid4(),
            amount=amount,
            tip=request.tip,
            email=request.email,
            name=request.name,
            fiscal_info=request.fiscal_info,
            payment_method=request.payment_method,
            payment_type=request.payment_type,
            status="pending",
            dish_ids=request.item_ids,
            created_at=timestamp,
        )

        if order.status != OrderStatus.PAYING:
            order.start_payment(timestamp)
        order.add_payment(payment, timestamp)
        await self.order_repository.update(order)

        self.logger.info(
            "[public] Payment request %s for order %s — $%s", payment.id, order.id, amount
        )

        await self.event_bus.publish(
            table.group,
            Event(
                type="payment.requested",
                payload={
                    "table_id": str(table_id),
                    "table_number": table.number,
                    "order_id": str(order.id),
                    "payment_id": str(payment.id),
                    "amount": str(amount),
                    "tip": str(request.tip),
                    "payment_method": request.payment_method,
                    "payment_type": request.payment_type,
                    "customer_name": request.name,
                },
            ),
        )

        return Response(payment_id=payment.id, amount=amount, status="pending")

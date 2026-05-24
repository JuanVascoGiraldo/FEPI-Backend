from logging import Logger
from uuid import UUID, uuid4

from app.domain.aggregate.order.order_item import OrderItem
from app.domain.aggregate.order.order_item_status import OrderItemStatus
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.exceptions import OrderNotFoundException, PaymentNotFoundException
from app.domain.repositories.order_repository import OrderRepository
from app.domain.repositories.table_repository import TableRepository
from app.domain.services.email_service import EmailService
from app.infrastructure.events.event_bus import EventBus, Event

from .response import Response


class Handler:
    def __init__(
        self,
        order_repository: OrderRepository,
        table_repository: TableRepository,
        email_service: EmailService,
        event_bus: EventBus,
        logger: Logger,
    ) -> None:
        self.order_repository = order_repository
        self.table_repository = table_repository
        self.email_service = email_service
        self.event_bus = event_bus
        self.logger = logger

    async def handle(self, order_id: UUID, payment_id: UUID, session: Meta) -> Response:
        timestamp = session.timestamp

        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(str(order_id))

        payment = next((p for p in order.payments if p.id == payment_id), None)
        if not payment:
            raise PaymentNotFoundException(str(payment_id))

        payment.status = "confirmed"
        order.waiter_id = session.user_id

        receipt_items: list[OrderItem] = []

        if payment.payment_type == "items" and payment.item_quantities:
            # Build receipt snapshot before mutating quantities
            for item_id_str, paid_qty in payment.item_quantities.items():
                item = order.get_item(UUID(item_id_str))
                if item is None:
                    continue
                actual_qty = min(paid_qty, item.quantity)
                receipt_items.append(item.model_copy(update={"quantity": actual_qty}))

            # Apply partial payment: split items so total() stays consistent
            new_paid_items: list[OrderItem] = []
            for item_id_str, paid_qty in payment.item_quantities.items():
                item = order.get_item(UUID(item_id_str))
                if item is None:
                    continue
                actual_qty = min(paid_qty, item.quantity)
                if actual_qty >= item.quantity:
                    item.status = OrderItemStatus.PAID
                else:
                    item.quantity -= actual_qty
                    new_paid_items.append(OrderItem(
                        id=uuid4(),
                        dish_id=item.dish_id,
                        name=item.name,
                        unit_price=item.unit_price,
                        quantity=actual_qty,
                        specifications=item.specifications,
                        status=OrderItemStatus.PAID,
                    ))
            order.items.extend(new_paid_items)

        elif payment.payment_type == "items" and payment.dish_ids:
            item_set = set(payment.dish_ids)
            for item in order.items:
                if item.id in item_set:
                    item.status = OrderItemStatus.PAID
            receipt_items = [i for i in order.items if i.id in item_set]

        else:
            receipt_items = [
                i for i in order.items if i.status != OrderItemStatus.CANCELLED
            ]

        order.updated_at = timestamp

        if order.is_fully_paid():
            order.close(timestamp)

        await self.order_repository.update(order)

        table = await self.table_repository.get_by_id(order.table_id)
        table_number = table.number if table else "?"

        if not receipt_items:
            receipt_items = [
                i for i in order.items if i.status != OrderItemStatus.CANCELLED
            ]

        try:
            await self.email_service.send_receipt(
                to=str(payment.email),
                name=payment.name,
                table_number=table_number,
                amount=payment.amount,
                tip=payment.tip,
                items=receipt_items,
                fiscal_info=payment.fiscal_info,
                payment_method=payment.payment_method,
            )
        except Exception as exc:
            self.logger.error("Receipt email failed for payment %s: %s", payment_id, exc)

        await self.event_bus.publish(
            order.group,
            Event(
                type="payment.confirmed",
                payload={
                    "table_number": table_number,
                    "order_id": str(order_id),
                    "payment_id": str(payment_id),
                    "fully_paid": order.is_fully_paid(),
                    "customer_name": payment.name,
                    "amount": float(payment.amount),
                },
            ),
        )

        self.logger.info(
            "Payment %s confirmed for order %s (fully_paid=%s)", payment_id, order_id, order.is_fully_paid()
        )

        return Response(
            order_id=order_id,
            payment_id=payment_id,
            fully_paid=order.is_fully_paid(),
            order_status=int(order.status),
        )

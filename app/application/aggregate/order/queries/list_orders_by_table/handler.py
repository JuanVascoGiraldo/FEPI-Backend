from logging import Logger
from uuid import UUID

from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.user.user_role import UserRole
from app.domain.exceptions import IsNotAuthorizedException
from app.domain.repositories.order_repository import OrderRepository

from .response import OrderItemResponse, OrderResponse, PaymentResponse, Response


class Handler:
    def __init__(self, order_repository: OrderRepository, logger: Logger) -> None:
        self.order_repository = order_repository
        self.logger = logger

    async def handle(self, table_id: UUID, session: Meta) -> Response:
        if session.role not in (UserRole.ADMIN, UserRole.WAITER):
            raise IsNotAuthorizedException()

        orders = await self.order_repository.get_by_table_id(table_id)

        return Response(
            orders=[
                OrderResponse(
                    id=o.id,
                    group=o.group,
                    table_id=o.table_id,
                    waiter_id=o.waiter_id,
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
                        for i in o.items
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
                        for p in o.payments
                    ],
                    status=int(o.status),
                    notes=o.notes,
                    total=o.total(),
                    total_paid=o.total_paid(),
                    total_pending=o.total_pending(),
                    created_at=o.created_at,
                    updated_at=o.updated_at,
                )
                for o in orders
            ]
        )

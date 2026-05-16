from logging import Logger

from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.user.user_role import UserRole
from app.domain.exceptions import IsNotAuthorizedException
from app.domain.repositories.order_repository import OrderRepository
from app.domain.repositories.table_repository import TableRepository

from .response import OrderItemResponse, OrderResponse, PaymentResponse, Response


class Handler:
    def __init__(
        self,
        order_repository: OrderRepository,
        table_repository: TableRepository,
        logger: Logger,
    ) -> None:
        self.order_repository = order_repository
        self.table_repository = table_repository
        self.logger = logger

    async def handle(self, session: Meta) -> Response:
        if session.role not in (UserRole.ADMIN, UserRole.WAITER):
            raise IsNotAuthorizedException()

        orders = await self.order_repository.get_by_group(session.group)
        tables = await self.table_repository.get_by_group(session.group)
        table_map = {str(t.id): t.number for t in tables}

        return Response(
            orders=[
                OrderResponse(
                    id=o.id,
                    table_id=o.table_id,
                    table_number=table_map.get(str(o.table_id), "?"),
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
                            email=str(p.email),
                            name=p.name,
                            payment_method=p.payment_method,
                            payment_type=p.payment_type,
                            status=p.status,
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

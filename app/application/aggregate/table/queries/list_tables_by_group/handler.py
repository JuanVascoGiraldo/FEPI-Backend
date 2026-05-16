from logging import Logger

from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.user.user_role import UserRole
from app.domain.exceptions import IsNotAuthorizedException
from app.domain.repositories.table_repository import TableRepository
from app.domain.repositories.order_repository import OrderRepository

from .response import ActiveOrderResponse, OrderItemResponse, PaymentResponse, Response, TableResponse


class Handler:
    def __init__(
        self,
        table_repository: TableRepository,
        order_repository: OrderRepository,
        logger: Logger,
    ) -> None:
        self.table_repository = table_repository
        self.order_repository = order_repository
        self.logger = logger

    async def handle(self, session: Meta) -> Response:
        if session.role not in (UserRole.ADMIN, UserRole.WAITER):
            raise IsNotAuthorizedException()

        tables = await self.table_repository.get_by_group(session.group)

        result = []
        for table in tables:
            active_order = await self.order_repository.get_open_by_table(table.id)

            active_order_response = None
            if active_order is not None:
                active_order_response = ActiveOrderResponse(
                    id=active_order.id,
                    waiter_id=active_order.waiter_id,
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
                        for i in active_order.items
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
                        for p in active_order.payments
                    ],
                    status=int(active_order.status),
                    notes=active_order.notes,
                    total=active_order.total(),
                    total_paid=active_order.total_paid(),
                    total_pending=active_order.total_pending(),
                    created_at=active_order.created_at,
                    updated_at=active_order.updated_at,
                )

            result.append(
                TableResponse(
                    id=table.id,
                    number=table.number,
                    description=table.description,
                    status=int(table.status),
                    active_order=active_order_response,
                    created_at=table.created_at,
                    updated_at=table.updated_at,
                )
            )

        return Response(tables=result)

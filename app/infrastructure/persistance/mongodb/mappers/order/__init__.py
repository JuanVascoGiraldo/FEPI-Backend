from app.domain.aggregate.order import Order, OrderItem, OrderStatus, OrderItemStatus
from app.infrastructure.persistance.mongodb.dao.order_dao import OrderDao
from app.infrastructure.persistance.mongodb.dao.order_item_dao import OrderItemDao


def from_order_item_to_dao(item: OrderItem) -> OrderItemDao:
    return OrderItemDao(
        id=item.id,
        dish_id=item.dish_id,
        name=item.name,
        unit_price=item.unit_price,
        quantity=item.quantity,
        specifications=item.specifications,
        amount_paid=item.amount_paid,
        status=int(item.status),
    )


def from_dao_to_order_item(dao: OrderItemDao) -> OrderItem:
    return OrderItem(
        id=dao.id,
        dish_id=dao.dish_id,
        name=dao.name,
        unit_price=dao.unit_price,
        quantity=dao.quantity,
        specifications=dao.specifications,
        amount_paid=dao.amount_paid,
        status=OrderItemStatus(dao.status),
    )


def from_order_to_dao(order: Order) -> OrderDao:
    return OrderDao(
        id=order.id,
        group=order.group,
        table_id=order.table_id,
        waiter_id=order.waiter_id,
        items=[from_order_item_to_dao(i) for i in order.items],
        status=int(order.status),
        notes=order.notes,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


def from_dao_to_order(dao: OrderDao) -> Order:
    return Order(
        id=dao.id,
        group=dao.group,
        table_id=dao.table_id,
        waiter_id=dao.waiter_id,
        items=[from_dao_to_order_item(i) for i in dao.items],
        status=OrderStatus(dao.status),
        notes=dao.notes,
        created_at=dao.created_at,
        updated_at=dao.updated_at,
    )

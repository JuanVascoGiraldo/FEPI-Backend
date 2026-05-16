from app.domain.aggregate.order import Order, OrderItem, OrderStatus, OrderItemStatus, Payment
from app.infrastructure.persistance.mongodb.dao.order_dao import OrderDao
from app.infrastructure.persistance.mongodb.dao.order_item_dao import OrderItemDao
from app.infrastructure.persistance.mongodb.dao.payment_dao import PaymentDao


def from_order_item_to_dao(item: OrderItem) -> OrderItemDao:
    return OrderItemDao(
        id=item.id,
        dish_id=item.dish_id,
        name=item.name,
        unit_price=item.unit_price,
        quantity=item.quantity,
        specifications=item.specifications,
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
        status=OrderItemStatus(dao.status),
    )


def from_payment_to_dao(payment: Payment) -> PaymentDao:
    return PaymentDao(
        id=payment.id,
        amount=payment.amount,
        tip=payment.tip,
        email=payment.email,
        name=payment.name,
        fiscal_info=payment.fiscal_info,
        payment_method=payment.payment_method,
        payment_type=payment.payment_type,
        status=payment.status,
        dish_ids=payment.dish_ids,
        created_at=payment.created_at,
    )


def from_dao_to_payment(dao: PaymentDao) -> Payment:
    return Payment(
        id=dao.id,
        amount=dao.amount,
        tip=dao.tip,
        email=dao.email,
        name=dao.name,
        fiscal_info=dao.fiscal_info,
        payment_method=dao.payment_method,
        payment_type=dao.payment_type,
        status=dao.status,
        dish_ids=dao.dish_ids,
        created_at=dao.created_at,
    )


def from_order_to_dao(order: Order) -> OrderDao:
    return OrderDao(
        id=order.id,
        group=order.group,
        table_id=order.table_id,
        waiter_id=order.waiter_id,
        items=[from_order_item_to_dao(i) for i in order.items],
        payments=[from_payment_to_dao(p) for p in order.payments],
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
        payments=[from_dao_to_payment(p) for p in dao.payments],
        status=OrderStatus(dao.status),
        notes=dao.notes,
        created_at=dao.created_at,
        updated_at=dao.updated_at,
    )

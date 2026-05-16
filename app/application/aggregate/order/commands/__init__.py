from fastapi import APIRouter

from . import create_order, add_item, remove_item, confirm_payment, mark_item_delivered

router = APIRouter()
router.include_router(create_order.router)
router.include_router(add_item.router)
router.include_router(remove_item.router)
router.include_router(confirm_payment.router)
router.include_router(mark_item_delivered.router)

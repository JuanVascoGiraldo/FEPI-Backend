from fastapi import APIRouter

from . import list_orders_by_table

router = APIRouter(tags=["order-queries"])

router.include_router(list_orders_by_table.router)

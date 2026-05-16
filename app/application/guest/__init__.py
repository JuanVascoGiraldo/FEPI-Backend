from fastapi import APIRouter

from . import get_table_menu, add_item_public, request_payment

router = APIRouter(prefix="/public")

router.include_router(get_table_menu.router)
router.include_router(add_item_public.router)
router.include_router(request_payment.router)

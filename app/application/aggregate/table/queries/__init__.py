from fastapi import APIRouter

from . import list_tables_by_group

router = APIRouter(tags=["table-queries"])

router.include_router(list_tables_by_group.router)

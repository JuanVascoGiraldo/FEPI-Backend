from fastapi import APIRouter

from . import create_table

router = APIRouter(tags=["table-commands"])

router.include_router(create_table.router)

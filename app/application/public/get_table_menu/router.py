from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import get_dependency

from .handler import Handler
from .response import Response

router = APIRouter()


@router.get("/table/{table_id}", response_model=Response, status_code=status.HTTP_200_OK)
async def get_table_menu(table_id: UUID) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(table_id)

from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.dependencies import get_dependency
from app.infrastructure.inyections import get_session_meta
from app.domain.aggregate.value_objects.meta import Meta

from .handler import Handler
from .response import Response

router = APIRouter()


@router.get("/by-table/{table_id}", response_model=Response, status_code=status.HTTP_200_OK)
async def list_orders_by_table(table_id: UUID, session: Meta = Depends(get_session_meta)) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(table_id, session)

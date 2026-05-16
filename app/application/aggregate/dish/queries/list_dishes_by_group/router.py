from fastapi import APIRouter, status, Depends

from app.dependencies import get_dependency
from app.infrastructure.inyections import get_session_meta
from app.domain.aggregate.value_objects.meta import Meta

from .handler import Handler
from .response import Response


router = APIRouter()


@router.get("/", response_model=Response, status_code=status.HTTP_200_OK)
async def list_dishes(session: Meta = Depends(get_session_meta)):
    handler: Handler = get_dependency(Handler)
    return await handler.handle(session)

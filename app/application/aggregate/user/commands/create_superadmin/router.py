from fastapi import APIRouter, status, Depends

from app.dependencies import get_dependency
from app.infrastructure.inyections import get_session_meta
from app.domain.aggregate.value_objects.meta import Meta

from .handler import Handler
from .request import Request
from .response import Response
from datetime import datetime, timezone

router = APIRouter()


@router.post("/superadmin", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create_superadmin(request: Request, 
                            # session: Meta = Depends(get_session_meta)
        ) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(request, datetime.now(timezone.utc))

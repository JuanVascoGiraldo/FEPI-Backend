from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_dependency, get_session_meta
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.settings.group_settings import GroupSettings
from app.domain.repositories.settings_repository import SettingsRepository

router = APIRouter(prefix="/settings")


class SettingsResponse(BaseModel):
    restaurant_name: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: str = "#f59e0b"


class UpdateSettingsRequest(BaseModel):
    restaurant_name: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None


@router.get("/", response_model=SettingsResponse)
async def get_settings(session: Meta = Depends(get_session_meta)):
    repo = get_dependency(SettingsRepository)
    settings = await repo.get_by_group(session.group)
    if not settings:
        return SettingsResponse()
    return SettingsResponse(
        restaurant_name=settings.restaurant_name,
        logo_url=settings.logo_url,
        primary_color=settings.primary_color,
    )


@router.put("/", response_model=SettingsResponse)
async def update_settings(
    body: UpdateSettingsRequest,
    session: Meta = Depends(get_session_meta),
):
    repo = get_dependency(SettingsRepository)
    existing = await repo.get_by_group(session.group) or GroupSettings(group=session.group)
    updated = existing.model_copy(update={
        k: v for k, v in body.model_dump().items() if v is not None
    })
    await repo.upsert(updated)
    return SettingsResponse(
        restaurant_name=updated.restaurant_name,
        logo_url=updated.logo_url,
        primary_color=updated.primary_color,
    )

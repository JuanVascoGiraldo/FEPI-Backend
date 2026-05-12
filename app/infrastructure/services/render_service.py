import re
from pathlib import Path

from app.domain.services.render_service import RenderService

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_PLACEHOLDER = re.compile(r"\{\{(.+?)\}\}")


class RenderServiceImpl(RenderService):

    def __init__(self) -> None:
        pass

    def render(self, template_name: str, context: dict) -> str:
        path = _TEMPLATES_DIR / template_name
        html = path.read_text(encoding="utf-8")

        def _replace(match: re.Match) -> str:
            key = match.group(1).strip()
            value = context.get(key)
            return str(value) if value is not None else ""

        return _PLACEHOLDER.sub(_replace, html)

from abc import ABC, abstractmethod


class RenderService(ABC):

    @abstractmethod
    def render(self, template_name: str, context: dict) -> str:
        """Load a template by name and substitute {{variable}} placeholders."""
        pass

from typing import Protocol, List, Optional
from architext.core.domain.entities.world_template import WorldTemplate

class WorldTemplateRepository(Protocol):
    def get_world_template_by_id(self, world_template_id: str) -> Optional[WorldTemplate]:
        ...

    def save_world_template(self, template: WorldTemplate) -> None:
        ...

    def delete_world_template(self, world_template_id: str) -> None:
        ...

    def list_world_templates(self) -> List[WorldTemplate]:
        ...

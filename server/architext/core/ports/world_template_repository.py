from typing import Protocol, List, Optional
from architext.core.domain.entities.world_template import WorldTemplate

class WorldTemplateRepository(Protocol):
    def get_world_template_by_id(self, template_id: str) -> Optional[WorldTemplate]:
        pass

    def save_world_template(self, template: WorldTemplate) -> None:
        pass

    def delete_world_template(self, template_id: str) -> None:
        pass

    def list_world_templates(self) -> List[WorldTemplate]:
        pass

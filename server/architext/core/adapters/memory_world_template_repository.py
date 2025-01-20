from typing import Dict, List, Optional
from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.ports.world_template_repository import WorldTemplateRepository
from copy import deepcopy


class MemoryWorldTemplateRepository(WorldTemplateRepository):
    def __init__(self) -> None:
        self._world_templates: Dict[str, WorldTemplate] = {}

    def get_world_template_by_id(self, world_template_id: str) -> Optional[WorldTemplate]:
        return deepcopy(self._world_templates.get(world_template_id, None))

    def save_world_template(self, world_template: WorldTemplate) -> None:
        self._world_templates[world_template.id] = deepcopy(world_template)

    def delete_world_template(self, world_template_id: str) -> None:
        del self._world_templates[world_template_id]

    def list_world_templates(self) -> List[WorldTemplate]:
        return deepcopy(list(self._world_templates.values()))

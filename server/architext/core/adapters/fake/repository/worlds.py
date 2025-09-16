from typing import Dict, List, Optional
from architext.core.domain.entities.world import World
from architext.core.application.ports.repository.worlds import WorldRepository
from copy import deepcopy


class MemoryWorldRepository(WorldRepository):
    def __init__(self) -> None:
        self._worlds: Dict[str, World] = {}

    def get_world_by_id(self, world_id: str) -> Optional[World]:
        return deepcopy(self._worlds.get(world_id, None))

    def save_world(self, world: World) -> None:
        self._worlds[world.id] = deepcopy(world)

    def delete_world(self, world_id: str) -> None:
        del self._worlds[world_id]

    def list_worlds(self) -> List[World]:
        return deepcopy(list(self._worlds.values()))

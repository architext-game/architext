from typing import Protocol, List, Optional
from architext.core.domain.entities.world import World

class WorldRepository(Protocol):
    def get_world_by_id(self, world_id: str) -> Optional[World]:
        pass

    def save_world(self, world: World) -> None:
        pass

    def delete_world(self, world_id: str) -> None:
        pass

    def list_worlds(self) -> List[World]:
        pass

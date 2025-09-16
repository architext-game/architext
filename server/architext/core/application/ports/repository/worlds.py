from typing import Protocol, List, Optional
from architext.core.domain.entities.world import World

class WorldRepository(Protocol):
    def get_world_by_id(self, world_id: str) -> Optional[World]:
        ...

    def save_world(self, world: World) -> None:
        ...

    def delete_world(self, world_id: str) -> None:
        ...

    def list_worlds(self) -> List[World]:
        ...

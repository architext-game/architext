from typing import List, Optional
from dataclasses import dataclass, field
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.item import Item

@dataclass(frozen=True)
class Room:
    id: str
    name: str
    world_id: str
    description: str = field(default="")
    exits: List[Exit] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)

    def get_exit_destination_id(self, exit_name: str) -> Optional[str]:
        return next((ext.destination_room_id for ext in self.exits if ext.name == exit_name), None)
    
    def with_replaced_exit(self, old: Exit, new: Exit):
        exits = [exit for exit in self.exits if exit.name != old.name] + [new]
        return self.with_changes(exits=exits)
    
    def with_changes(
        self, 
        name: Optional[str] = None,
        description: Optional[str] = None,
        exits: Optional[List[Exit]] = None,
        items: Optional[List[Item]] = None
    ) -> "Room":
        return Room(
            id=self.id,
            world_id=self.world_id,
            name=name if name else self.name,
            description=description if description else self.description,
            exits=exits if exits else self.exits,
            items=items if items else self.items,
        )


DEFAULT_ROOM = Room(
    id="DEFAULT_ROOM",
    name="Initial room",
    description="This is the initial room.",
    exits=[],
    world_id="DEFAULT_WORLD"
)
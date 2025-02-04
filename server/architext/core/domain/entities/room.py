from types import MappingProxyType
from typing import List, Mapping, Optional
from dataclasses import dataclass, field
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.item import Item

@dataclass(frozen=True)
class Room:
    id: str
    name: str
    world_id: str
    description: str = field(default="")
    exits: Mapping[str, Exit] = field(default_factory=dict)
    items: Mapping[str, Item] = field(default_factory=dict)

    def __post_init__(self):
        # Guarantee that exits and items are immutable
        object.__setattr__(self, "exits", MappingProxyType(dict(self.exits)))
        object.__setattr__(self, "items", MappingProxyType(dict(self.items)))

    def with_replaced_exit(self, old: Exit, new: Exit) -> 'Room':
        new_exits = {name: exit for name, exit in self.exits.items() if name != old.name}
        new_exits[new.name] = new
        
        return self.with_changes(exits=new_exits)

    def with_exit(self, exit: Exit) -> 'Room':
        new_exits = {name: exit for name, exit in self.exits.items()}
        new_exits[exit.name] = exit
        
        return self.with_changes(exits=new_exits)
    
    def with_item(self, item: Item) -> 'Room':
        new_items = {name: item for name, item in self.items.items()}
        new_items[item.name] = item

        return self.with_changes(items=new_items)
    
    def with_changes(
        self, 
        name: Optional[str] = None,
        description: Optional[str] = None,
        exits: Optional[Mapping[str, Exit]] = None,
        items: Optional[Mapping[str, Item]] = None
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
    exits={},
    world_id="DEFAULT_WORLD"
)
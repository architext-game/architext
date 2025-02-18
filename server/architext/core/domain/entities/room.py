from types import MappingProxyType
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.item import Item
from architext.core.domain.names import duplicates

@dataclass
class Room:
    id: str
    name: str
    world_id: str
    description: str = field(default="")
    exits: Dict[str, Exit] = field(default_factory=dict)
    items: Dict[str, Item] = field(default_factory=dict)

    def __post_init__(self):        
        self._assert_no_duplicated_room_or_exit_names()

    def _assert_no_duplicated_room_or_exit_names(self):
        if duplicates(list(self.exits.keys()) + list(self.items.keys())):
            raise DuplicatedNameInRoom()

    def replace_exit(self, old: Exit, new: Exit) -> None:
        exit_names = set(self.exits.keys()) - {old.name}
        if duplicates(list(exit_names) + list(self.items.keys()) + [new.name]):
            raise DuplicatedNameInRoom(f"Cannot replace with new name '{new.name}', name is in use in this room.")
        del self.exits[old.name]
        self.exits[new.name] = new

    def add_exit(self, exit: Exit) -> None:
        if duplicates(list(self.exits.keys()) + list(self.items.keys()) + [exit.name]):
            raise DuplicatedNameInRoom(f"Cannot add exit '{exit.name}', name is in use in this room.")
        
        self.exits[exit.name] = exit

    def remove_exit(self, exit_to_delete: Exit) -> None:
        del self.exits[exit_to_delete.name]
    
    def replace_item(self, old: Item, new: Item) -> None:
        item_names = set(self.items.keys()) - {old.name}
        if duplicates(list(item_names) + list(self.exits.keys()) + [new.name]):
            raise DuplicatedNameInRoom(f"Cannot replace with new name '{new.name}', name is in use in this room.")
        del self.items[old.name]
        self.items[new.name] = new

    def can_add_item(self, item: Item) -> None:
        if duplicates(list(self.exits.keys()) + list(self.items.keys()) + [item.name]):
            raise DuplicatedNameInRoom(f"Cannot add item '{item.name}', name is in use in this room.")

    def add_item(self, item: Item) -> None:
        if duplicates(list(self.exits.keys()) + list(self.items.keys()) + [item.name]):
            raise DuplicatedNameInRoom(f"Cannot add item '{item.name}', name is in use in this room.")
        self.items[item.name] = item

    def remove_item(self, item_to_delete: Item) -> None:
        del self.items[item_to_delete.name]


DEFAULT_ROOM = Room(
    id="DEFAULT_ROOM",
    name="Initial room",
    description="This is the initial room.",
    exits={},
    world_id="DEFAULT_WORLD"
)


class DuplicatedNameInRoom(Exception):
    def __init__(self, message="Tried to instantiate room with a duplicated item and/or exit name."):
        super().__init__(message)


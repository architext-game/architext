from typing import List, Optional
from dataclasses import dataclass, field
from architext.clean.domain.entities.exit import Exit

@dataclass
class Room:
    id: str
    name: str
    description: str = field(default="")
    exits: List[Exit] = field(default_factory=list)

    def get_exit_destination_id(self, exit_name: str) -> Optional[str]:
        return next((exit.destination_room_id for exit in self.exits if exit.name == exit_name), None)
    

DEFAULT_ROOM = Room(
    id="DEFAULT",
    name="Initial room",
    description="This is the initial room.",
    exits=[]
)
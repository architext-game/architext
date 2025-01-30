from typing import List, Literal, Optional
from dataclasses import dataclass, field
from architext.core.domain.entities.exit import Exit

@dataclass
class World:
    id: str
    name: str
    initial_room_id: str
    owner_user_id: Optional[str]  # null if it is a predefined world
    description: str = field(default="")
    visibility: Literal["public", "private"] = field(default="private")
    base_template_id: Optional[str] = field(default=None)


DEFAULT_WORLD = World(
    name="Initial world",
    description="This world is a predefined world",
    id="DEFAULT_WORLD",
    initial_room_id="DEFAULT_ROOM",
    owner_user_id=None,
)

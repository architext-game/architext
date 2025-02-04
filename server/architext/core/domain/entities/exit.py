from dataclasses import dataclass
from architext.core.domain.primitives import Visibility

@dataclass(frozen=True)
class Exit:
    """Exits are part of the Room aggregate"""
    name: str
    description: str
    destination_room_id: str
    visibility: Visibility = "auto"

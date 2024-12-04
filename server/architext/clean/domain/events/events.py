from dataclasses import dataclass
from typing import TypeVar, Optional

class Event:
    pass


@dataclass
class UserChangedRoom(Event):
    user_id: str
    room_entered: Optional[str] = None
    room_left: Optional[str] = None
    exit_used: Optional[str] = None

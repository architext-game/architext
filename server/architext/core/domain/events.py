"""
The events that can happen in our system (see messagebus).
"""


from dataclasses import dataclass
from typing import Literal, Optional

class Event:
    pass

@dataclass
class UserChangedRoom(Event):
    user_id: str
    room_entered: Optional[str] = None
    room_left: Optional[str] = None
    exit_used: Optional[str] = None

@dataclass
class WorldCreationRequested(Event):
    user_id: str
    world_name: str
    world_description: str
    text_representation: str
    format: Literal['plain', 'encoded']


@dataclass
class WorldCreated(Event):
    owner_id: str
    world_id: str


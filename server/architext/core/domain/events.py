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
    method: Literal["used_exit", "teleported", "changed_world"]
    room_entered_id: Optional[str] = None
    room_left_id: Optional[str] = None
    exit_used_name: Optional[str] = None

@dataclass
class WorldCreationRequested(Event):
    future_world_id: str
    world_name: str
    world_description: str
    text_representation: str
    format: Literal['plain', 'encoded']
    visibility: Literal['public', 'private']
    user_id: Optional[str] = None
    base_template_id: Optional[str] = None  # just used to add the reference to the new world

@dataclass
class WorldCreated(Event):
    owner_id: Optional[str]
    world_id: str

@dataclass
class UserCreated(Event):
    user_id: str

"""
The following events don't have a handler defined by the core.
The core delegates the handling of this events to external
handlers that should be provided by the core's client.
"""
@dataclass
class ShouldNotifyUserEnteredRoom(Event):
    to_user_id: str
    through_exit_name: Optional[str]
    entered_world: bool
    user_name: str

@dataclass
class ShouldNotifyUserLeftRoom(Event):
    to_user_id: str
    through_exit_name: Optional[str]
    movement: Literal['used_exit', 'teleported', 'disconnected', 'left_world']
    user_name: str

@dataclass
class ShouldNotifyWorldCreated(Event):
    to_user_id: str
    world_id: str
    world_name: str

@dataclass
class UserBecameActive(Event):
    user_id: str
    user_name: str
    room_id: str

@dataclass
class UserBecameInactive(Event):
    user_id: str
    user_name: str
    room_id: str


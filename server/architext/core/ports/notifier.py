"""
This module defines the Notifier port, which is used to notify users of events that happened in the game.
"""

from dataclasses import dataclass
from typing import Literal, Optional, Protocol

@dataclass
class Notification(Protocol):
    pass

@dataclass
class WorldCreatedNotification(Notification):
    world_id: str

@dataclass
class UserEnteredRoomNotification(Notification):
    through_exit_name: Optional[str]
    movement: Literal['used_exit', 'teleported', 'reconnected', 'entered_world']
    user_name: str

@dataclass
class UserLeftRoomNotification(Notification):
    through_exit_name: Optional[str]
    movement: Literal['used_exit', 'teleported', 'disconnected', 'left_world']
    user_name: str

@dataclass
class SocialInteractionNotification(Notification):
    kind: Literal['talk', 'emote']
    content: str
    user_name: str
    
class Notifier(Protocol):
    def notify(self, user_id: str, notification: Notification):
        ...
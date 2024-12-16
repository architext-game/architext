"""
# Handlers module

 - This module defines the event handlers used by the messagebus.
 - It also links events with their handlers in the `EVENT_HANDLERS` dict.
"""

from architext.core.domain.events import UserChangedRoom, Event
from architext.core.commands import Command
from architext.core.handlers.notify_other_entered_room import notify_other_entered_room
from architext.core.handlers.notify_other_left_room import notify_other_left_room
from typing import Any, Callable, Dict, Type, List, Union, TypeVar
from architext.ports.unit_of_work import UnitOfWork


EVENT_HANDLERS: Dict[Type[Event], List[Callable]] = {
    UserChangedRoom: [notify_other_entered_room, notify_other_left_room]
}
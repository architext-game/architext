"""
# Handlers module

 - This module defines the event handlers used by the messagebus.
 - It also links events with their handlers in the `EVENT_HANDLERS` dict.
"""

from architext.core.domain.events import UserBecameActive, UserBecameInactive, UserChangedRoom, Event, WorldCreated, WorldCreationRequested
from architext.core.handlers.notify_other_became_inactive import notify_other_became_inactive
from architext.core.handlers.notify_other_became_active import notify_other_became_active
from architext.core.handlers.notify_world_created import notify_world_created
from architext.core.handlers.notify_other_entered_room import notify_other_entered_room
from architext.core.handlers.notify_other_left_room import notify_other_left_room
from architext.core.handlers.import_world import import_world
from typing import Any, Callable, Dict, Type, List


EVENT_HANDLERS: Dict[Type[Event], List[Callable]] = {
    UserChangedRoom: [notify_other_entered_room, notify_other_left_room],
    UserBecameActive: [notify_other_became_active],
    UserBecameInactive: [notify_other_became_inactive],

    # The following events are raised as external events in production
    # They are only here so that all functionality works in testing
    # without an external message queue
    # > Published by server, handled by worker
    WorldCreationRequested: [import_world],
    # > Published by worker, handled by server
    WorldCreated: [notify_world_created],  # from worker to server
}
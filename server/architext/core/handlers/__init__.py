from architext.core.domain.events import UserChangedRoom
from architext.core.handlers.notify_other_entered_room import notify_other_entered_room
from architext.core.handlers.notify_other_left_room import notify_other_left_room

HANDLERS = {
    UserChangedRoom: [notify_other_entered_room, notify_other_left_room]
}
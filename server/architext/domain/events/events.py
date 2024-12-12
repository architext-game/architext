from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from architext.domain.unit_of_work.unit_of_work import UnitOfWork
else:
    UnitOfWork = object

class Event:
    pass

@dataclass
class UserChangedRoom(Event):
    user_id: str
    room_entered: Optional[str] = None
    room_left: Optional[str] = None
    exit_used: Optional[str] = None

@dataclass
class OtherEnteredRoomNotification:
    user_name: str


def notify_other_entered_room(uow: UnitOfWork, event: UserChangedRoom):
    if event.room_entered is None:
        return
    user_who_moved = uow.users.get_user_by_id(event.user_id)
    assert user_who_moved is not None
    users = uow.users.get_users_in_room(event.room_entered)
    for user in users:
        if user.id == event.user_id:
            continue
        uow.notifications.notify_user(
            user.id,
            'other_entered_room',
            OtherEnteredRoomNotification(user_name=user_who_moved.name)
        )


@dataclass
class OtherLeftRoomNotification:
    user_name: str


def notify_other_left_room(uow: UnitOfWork, event: UserChangedRoom):
    if event.room_left is None:
        return
    user_who_moved = uow.users.get_user_by_id(event.user_id)
    assert user_who_moved is not None
    users = uow.users.get_users_in_room(event.room_left)
    for user in users:
        if user.id == event.user_id:
            continue
        uow.notifications.notify_user(
            user.id,
            'other_left_room',
            OtherLeftRoomNotification(user_name=user_who_moved.name)
        )

HANDLERS = {
    UserChangedRoom: [notify_other_entered_room, notify_other_left_room]
}

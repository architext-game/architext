from dataclasses import dataclass, asdict
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import UserChangedRoom
from typing import List

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
            asdict(OtherEnteredRoomNotification(user_name=user_who_moved.name))
        )
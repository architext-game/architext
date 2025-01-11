from ast import List
from dataclasses import dataclass, asdict
from architext.core.domain.events import UserChangedRoom
from architext.core.ports.unit_of_work import UnitOfWork


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
            asdict(OtherLeftRoomNotification(user_name=user_who_moved.name))
        )
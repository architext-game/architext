from dataclasses import dataclass, asdict
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import ShouldNotifyUserEnteredRoom, UserChangedRoom
from typing import List

@dataclass
class OtherEnteredRoomNotification:
    user_name: str

def notify_other_entered_room(uow: UnitOfWork, event: UserChangedRoom):
    if event.room_entered_id is None:
        return
    user_who_moved = uow.users.get_user_by_id(event.user_id)
    assert user_who_moved is not None
    users = uow.users.get_users_in_room(event.room_entered_id)
    entered_room = uow.rooms.get_room_by_id(event.room_entered_id)
    assert entered_room is not None
    entered_through_exit = next((exit for exit in entered_room.exits.values() if exit.destination_room_id == event.room_left_id), None)
    
    for user in users:
        if user.id == event.user_id:
            continue
        uow.publish_events([ShouldNotifyUserEnteredRoom(
            to_user_id=user.id,
            user_name=user_who_moved.name,
            entered_world=event.room_left_id is None,
            through_exit_name=entered_through_exit.name if entered_through_exit else None
        )])

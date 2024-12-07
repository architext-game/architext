from architext.clean.domain.entities.room import Room
from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork
from typing import Optional

GetCurrentRoomOutput = Optional[Room]  # They are the same, but they may diverge in the future

def get_current_room(uow: UnitOfWork, client_user_id: str) -> Optional[GetCurrentRoomOutput]:
    with uow:
        user = uow.users.get_user_by_id(client_user_id)
        if user is None:
            raise ValueError("User is not in a room.")
        if user.room_id is None:
            current_room = None
        else:
            current_room = uow.rooms.get_room_by_id(user.room_id)
        uow.commit()

    return current_room
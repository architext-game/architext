from architext.clean.domain.entities.user import User
from architext.clean.domain.entities.room import Room
from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork

def get_current_room(uow: UnitOfWork, user: User) -> Room:
    if user.room_id is None:
        raise ValueError("User is not in a room.")
    
    with uow:
        current_room = uow.rooms.get_room_by_id(user.room_id)
        uow.commit()

    return current_room
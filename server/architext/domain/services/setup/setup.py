from architext.domain.unit_of_work.unit_of_work import UnitOfWork
from architext.domain.entities.room import Room, DEFAULT_ROOM


def setup(uow: UnitOfWork) -> None:
    """This service must be called before any other"""
    with uow:
        default_room = uow.rooms.get_room_by_id(DEFAULT_ROOM.id)
        if default_room is None:
            uow.rooms.save_room(DEFAULT_ROOM)
        uow.commit()

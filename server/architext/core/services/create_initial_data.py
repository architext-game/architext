from architext.ports.unit_of_work import UnitOfWork
from architext.core.domain.entities.room import Room, DEFAULT_ROOM
from architext.core.commands import CreateInitialData, CreateInitialDataResult


def create_initial_data(uow: UnitOfWork, command: CreateInitialData, client_user_id: str = "") -> CreateInitialDataResult:
    """This service must be called before any other"""
    with uow:
        default_room = uow.rooms.get_room_by_id(DEFAULT_ROOM.id)
        if default_room is None:
            uow.rooms.save_room(DEFAULT_ROOM)
        uow.commit()
    return CreateInitialDataResult()

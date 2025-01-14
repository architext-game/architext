from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.entities.room import DEFAULT_ROOM
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core.commands import CreateInitialData, CreateInitialDataResult


def create_initial_data(uow: UnitOfWork, command: CreateInitialData, client_user_id: str = "") -> CreateInitialDataResult:
    """This service must be called before any other"""
    with uow:
        default_world = uow.worlds.get_world_by_id(DEFAULT_WORLD.id)
        if default_world is None:
            uow.worlds.save_world(DEFAULT_WORLD)
            uow.rooms.save_room(DEFAULT_ROOM)
        uow.commit()
        default_world = uow.worlds.get_world_by_id(DEFAULT_WORLD.id)
    return CreateInitialDataResult()

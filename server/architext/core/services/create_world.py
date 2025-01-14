import copy
from architext.core.domain.entities.room import Room, DEFAULT_ROOM
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.world import World
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.commands import CreateWorld, CreateWorldRoomResult
from uuid import uuid4


def create_world(uow: UnitOfWork, command: CreateWorld, client_user_id: str) -> CreateWorldRoomResult:
    with uow:
        user = uow.users.get_user_by_id(client_user_id)
        assert user is not None
        world_id = str(uuid4())
        initial_room_id = str(uuid4())
        world = World(
            name=command.name,
            description=command.description,
            id=world_id,
            initial_room_id=initial_room_id,
            owner_user_id=user.id
        )
        
        initial_room = copy.deepcopy(DEFAULT_ROOM)
        initial_room.id = initial_room_id
        initial_room.world_id = world_id
        
        uow.rooms.save_room(initial_room)
        uow.worlds.save_world(world)
        
        uow.commit()

    return CreateWorldRoomResult(
        world_id=world_id
    )

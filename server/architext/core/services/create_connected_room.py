from architext.core.domain.entities.room import Room
from architext.core.domain.entities.exit import Exit
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.commands import CreateConnectedRoom, CreateConnectedRoomResult
from uuid import uuid4

from ..authorization import getUserAuthorizedInCurrentWorld

def create_connected_room(uow: UnitOfWork, command: CreateConnectedRoom, client_user_id: str) -> CreateConnectedRoomResult:
    with uow:
        user = getUserAuthorizedInCurrentWorld(uow, client_user_id)
        if not user:
            raise PermissionError("User is not in a world where she is authorized.")
        if user.room_id is None:
            raise ValueError("User needs to be in a room to create a connected room.")
        old_room = uow.rooms.get_room_by_id(user.room_id)
        assert old_room is not None
        new_room = Room(name=command.name, description=command.description, id=str(uuid4()), world_id=old_room.world_id)
        uow.rooms.save_room(new_room)
        old_room.exits.append(Exit(
            name=command.exit_to_new_room_name, 
            description=command.exit_to_new_room_description, 
            destination_room_id=new_room.id, 
        ))
        new_room.exits.append(Exit(
            name=command.exit_to_old_room_name, 
            description=command.exit_to_old_room_description, 
            destination_room_id=old_room.id, 
        ))

        uow.rooms.save_room(old_room)
        uow.rooms.save_room(new_room)

        uow.commit()

    return CreateConnectedRoomResult(
        room_id=new_room.id
    )

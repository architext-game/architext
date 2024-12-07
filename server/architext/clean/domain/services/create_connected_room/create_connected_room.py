from architext.clean.domain.entities.room import Room
from architext.clean.domain.entities.exit import Exit
from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork
from pydantic import BaseModel, Field
from uuid import uuid4

class CreateConnectedRoomInput(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    description: str = Field(max_length=3000)
    exit_to_new_room_name: str
    exit_to_new_room_description: str
    exit_to_old_room_name: str
    exit_to_old_room_description: str

CreateConnectedRoomOutput = Room

def create_connected_room(uow: UnitOfWork, input: CreateConnectedRoomInput, client_user_id: str) -> CreateConnectedRoomOutput:
    with uow:
        user = uow.users.get_user_by_id(client_user_id)
        assert user is not None and user.room_id is not None
        old_room = uow.rooms.get_room_by_id(user.room_id)
        new_room = Room(name=input.name, description=input.description, id=str(uuid4()))
        assert old_room is not None and new_room is not None
        uow.rooms.save_room(new_room)
        old_room.exits.append(Exit(
            name=input.exit_to_new_room_name, 
            description=input.exit_to_new_room_description, 
            destination_room_id=new_room.id, 
        ))
        new_room.exits.append(Exit(
            name=input.exit_to_old_room_name, 
            description=input.exit_to_old_room_description, 
            destination_room_id=old_room.id, 
        ))

        uow.rooms.save_room(old_room)
        uow.rooms.save_room(new_room)

        uow.commit()

    return new_room

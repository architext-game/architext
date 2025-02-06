from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.commands import EditRoom, EditRoomResult
from architext.core.domain.entities.room import Room
from architext.core.ports.unit_of_work import UnitOfWork


def edit_room(uow: UnitOfWork, command: EditRoom, client_user_id: str) -> EditRoomResult:
    with uow:
        assertUserIsAuthorizedInCurrentWorld(uow, client_user_id)
        user = uow.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        room = uow.rooms.get_room_by_id(command.room_id)

        if room is None:
            raise ValueError("Room does not exist")

        updated_room = room.with_changes(
            name=command.new_name,
            description=command.new_description
        )
        uow.rooms.save_room(updated_room)
        uow.commit()

    return EditRoomResult()
from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.commands import EditRoom, EditRoomResult
from architext.core.domain.entities.room import Room
from architext.core.ports.unit_of_work import UnitOfWork


def edit_room(uow: UnitOfWork, command: EditRoom, client_user_id: str) -> EditRoomResult:
    with uow as transaction:
        assertUserIsAuthorizedInCurrentWorld(transaction, client_user_id)
        user = transaction.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        room = transaction.rooms.get_room_by_id(command.room_id)

        if room is None:
            raise ValueError("Room does not exist")

        room.name = command.new_name if command.new_name else room.name
        room.description = command.new_description if command.new_description else room.description

        transaction.rooms.save_room(room)

    return EditRoomResult()
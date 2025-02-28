from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.commands import EditExit, EditExitResult
from architext.core.domain.entities.exit import Exit
from architext.core.ports.unit_of_work import UnitOfWork


def edit_exit(uow: UnitOfWork, command: EditExit, client_user_id: str) -> EditExitResult:
    with uow as transaction:
        assertUserIsAuthorizedInCurrentWorld(transaction, client_user_id)
        user = transaction.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        room = transaction.rooms.get_room_by_id(command.room_id)

        if room is None:
            raise ValueError("Room does not exist")

        exit = room.exits.get(command.exit_name, None)

        if exit is None:
            raise ValueError("Exit does not exist")
        
        new_exit = Exit(
            name=command.new_name if command.new_name else exit.name,
            description=command.new_description if command.new_description else exit.description,
            visibility=command.new_visibility if command.new_visibility else exit.visibility,
            destination_room_id=command.new_destination if command.new_destination else exit.destination_room_id,
        )

        room.replace_exit(exit, new_exit)
        transaction.rooms.save_room(room)

    return EditExitResult()
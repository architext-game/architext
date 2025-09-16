from architext.core.application.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.application.commands.delete_exit.command import DeleteExit, DeleteExitResult
from architext.core.domain.entities.exit import Exit
from architext.core.application.ports.unit_of_work import UnitOfWork


def delete_exit(uow: UnitOfWork, command: DeleteExit, client_user_id: str) -> DeleteExitResult:
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
        
        room.remove_exit(exit)
        transaction.rooms.save_room(room)

    return DeleteExitResult() 
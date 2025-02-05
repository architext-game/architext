from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.commands import DeleteExit, DeleteExitResult
from architext.core.domain.entities.exit import Exit
from architext.core.ports.unit_of_work import UnitOfWork


def delete_exit(uow: UnitOfWork, command: DeleteExit, client_user_id: str) -> DeleteExitResult:
    with uow:
        assertUserIsAuthorizedInCurrentWorld(uow, client_user_id)
        user = uow.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        room = uow.rooms.get_room_by_id(command.room_id)

        if room is None:
            raise ValueError("Room does not exist")

        exit = room.exits.get(command.exit_name, None)

        if exit is None:
            raise ValueError("Exit does not exist")
        
        updated_room = room.without_exit(exit)
        uow.rooms.save_room(updated_room)

        uow.commit()

    return DeleteExitResult()
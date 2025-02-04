from architext.core.commands import TraverseExit, TraverseExitResult
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import UserChangedRoom


def traverse_exit(uow: UnitOfWork, command: TraverseExit, client_user_id: str) -> TraverseExitResult:
    with uow:
        user = uow.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")

        if user.room_id is None:
            raise ValueError("User is not in a room.")
    
        previous_room = uow.rooms.get_room_by_id(user.room_id)
        assert previous_room is not None

        exit = previous_room.exits.get(command.exit_name, None)

        if exit is None:
            raise ValueError("An exit with that name was not found in the room.")

        destination_id = exit.destination_room_id
    
        user.room_id = destination_id
        uow.users.save_user(user)
        uow.publish_events([UserChangedRoom(user_id=user.id, exit_used=command.exit_name, room_entered=destination_id, room_left=previous_room.id)])
        uow.commit()

        return TraverseExitResult(new_room_id= user.room_id)
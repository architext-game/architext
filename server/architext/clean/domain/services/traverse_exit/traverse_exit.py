from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork
from architext.clean.domain.events.events import UserChangedRoom

def traverse_exit(uow: UnitOfWork, user_id: str, exit_name: str) -> str:
    with uow:
        user = uow.users.get_user_by_id(user_id=user_id)

        if user.room_id is None:
            raise ValueError("User is not in a room.")
    
        previous_room = uow.rooms.get_room_by_id(user.room_id)
        destination_id = previous_room.get_exit_destination_id(exit_name)
    
        if destination_id is None:
            raise ValueError("An exit with that name was not found in the room.")

        user.room_id = destination_id

        uow.publish_events([UserChangedRoom(user_id=user_id, exit_used=exit_name, room_entered=destination_id, room_left=previous_room.id)])

        return user.room_id
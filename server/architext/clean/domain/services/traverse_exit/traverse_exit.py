from architext.clean.domain.entities.user import User
from architext.clean.domain.repositories.room_repository import RoomRepository

def traverse_exit(room_repository: RoomRepository, user: User, exit_name: str) -> str:
    if user.room_id is None:
        raise ValueError("User is not in a room.")
    
    current_room = room_repository.get_room_by_id(user.room_id)
    exit_id = current_room.get_exit_destination_id(exit_name)
    
    if exit_id is None:
        raise ValueError("An exit with that name was not found in the room.")

    user.room_id = exit_id

    return user.room_id
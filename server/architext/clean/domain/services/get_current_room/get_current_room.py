from architext.clean.domain.entities.user import User
from architext.clean.domain.entities.room import Room
from architext.clean.domain.repositories.room_repository import RoomRepository

def get_current_room(room_repository: RoomRepository, user: User) -> Room:
    if user.room_id is None:
        raise ValueError("User is not in a room.")
    
    current_room = room_repository.get_room_by_id(user.room_id)
    return current_room
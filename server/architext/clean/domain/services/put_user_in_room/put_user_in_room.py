from architext.clean.domain.repositories.user_repository import UserRepository
from architext.clean.domain.repositories.room_repository import RoomRepository

def put_user_in_room(user_repository: UserRepository, room_repository: RoomRepository, user_id: str, room_id: str) -> None:
    user = user_repository.get_user_by_id(user_id)
    room = room_repository.get_room_by_id(room_id)

    if room is None:
        raise ValueError("The room does not exist")
    
    if user is None:
        raise ValueError("The user does not exist")
    
    user.room_id = room_id
    user_repository.save_user(user)

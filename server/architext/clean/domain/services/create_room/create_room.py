from architext.clean.domain.entities.room import Room
from architext.clean.domain.repositories.room_repository import RoomRepository

def create_room(room_repository: RoomRepository, name: str, id: str, description: str) -> str:
    # Business rule: validate user inputs
    # TODO

    room = Room(description=description, id=id, name=name)
    room_repository.save_room(room)

    return room.id

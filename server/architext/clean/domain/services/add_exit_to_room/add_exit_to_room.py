from architext.clean.domain.entities.exit import Exit
from architext.clean.domain.repositories.room_repository import RoomRepository

def add_exit_to_room(room_repository: RoomRepository, id: str, exit_name: str, destination_room_id: str) -> None:
    # Business rule: validate user inputs
    # TODO

    room = room_repository.get_room_by_id(id)
    room.exits.append(Exit(name=exit_name, destination_room_id=destination_room_id, description="", is_open=True, key_names=[], visibility='listed'))
    room_repository.save_room(room)

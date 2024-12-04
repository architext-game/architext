from architext.clean.domain.entities.exit import Exit
from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork

def add_exit_to_room(uow: UnitOfWork, id: str, exit_name: str, destination_room_id: str) -> None:
    with uow:
        room = uow.rooms.get_room_by_id(id)
        room.exits.append(Exit(name=exit_name, destination_room_id=destination_room_id, description="", is_open=True, key_names=[], visibility='listed'))
        uow.rooms.save_room(room)
        uow.commit()

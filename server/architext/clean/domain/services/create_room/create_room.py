from architext.clean.domain.entities.room import Room
from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork

def create_room(uow: UnitOfWork, name: str, id: str, description: str) -> str:
    with uow:
        room = Room(description=description, id=id, name=name)
        uow.rooms.save_room(room)
        uow.commit()

    return room.id

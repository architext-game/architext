from architext.clean.domain.entities.exit import Exit
from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork
from typing import Optional, List
from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class Person:
    id: str
    name: str

class GetCurrentRoomData(BaseModel):
    id: str
    name: str
    description: str
    exits: List[Exit]
    people: List[Person]

GetCurrentRoomOutput = Optional[GetCurrentRoomData]

def get_current_room(uow: UnitOfWork, client_user_id: str) -> GetCurrentRoomOutput:
    with uow:
        user = uow.users.get_user_by_id(client_user_id)
        if user is None:
            raise ValueError("User not found")
        if user.room_id is None:
            output = None
        else:
            current_room = uow.rooms.get_room_by_id(user.room_id)
            if current_room is None:
                raise ValueError("User is not in a room")
            users = uow.users.get_users_in_room(user.room_id)
            people_in_room = [Person(id=user.id, name=user.name) for user in users]
            output = GetCurrentRoomData(
                id=current_room.id,
                exits=current_room.exits,
                description=current_room.description,
                name=current_room.name,
                people=people_in_room
            )
        uow.commit()

    return output
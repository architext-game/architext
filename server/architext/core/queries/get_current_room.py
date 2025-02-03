from dataclasses import dataclass
from typing import Literal, List, Optional
from architext.core.authorization import assertUserIsLoggedIn
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.room import Room
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler

@dataclass
class PersonInRoom:
    id: str
    name: str

@dataclass
class ExitInRoom:
    name: str
    description: str
    visibility: Literal["unlisted", "listed"]

@dataclass
class CurrentRoom:
    id: str
    name: str
    description: str
    exits: List[ExitInRoom]
    people: List[PersonInRoom]

@dataclass
class GetCurrentRoomResult:
    current_room: Optional[CurrentRoom]

class GetCurrentRoom(Query[GetCurrentRoomResult]):
    pass

class GetCurrentRoomQueryHandler(QueryHandler[GetCurrentRoom, GetCurrentRoomResult]):
    pass

def visibility_filter(exit: Exit, room: Room) -> Literal["unlisted", "listed"]:
    if exit.visibility == "auto":
        if exit.name.lower() in room.description.lower():
            return "unlisted"
        else:
            return "listed"
    elif exit.visibility == "unlisted":
        return "unlisted"
    elif exit.visibility == "listed":
        return "listed"
    else:  # exit is hidden, this won't be in the query results
        return "unlisted"  

class UOWGetCurrentRoomQueryHandler(UOWQueryHandler, GetCurrentRoomQueryHandler):
    def query(self, query: GetCurrentRoom, client_user_id: str) -> GetCurrentRoomResult:
        uow = self._uow
        assertUserIsLoggedIn(uow, client_user_id)
        user = uow.users.get_user_by_id(client_user_id)
        if user is None:
            raise ValueError("User not found")
        if user.room_id is None:
            output = GetCurrentRoomResult(current_room=None)
        else:
            current_room = uow.rooms.get_room_by_id(user.room_id)
            if current_room is None:
                raise ValueError("User is not in a room")
            users = uow.users.get_users_in_room(user.room_id)
            people_in_room = [PersonInRoom(id=user.id, name=user.name) for user in users]
            exits_in_room = [ExitInRoom(
                name=exit.name, 
                description=exit.description,
                visibility=visibility_filter(exit, current_room),
            ) for exit in current_room.exits if exit.visibility != "hidden"]
            output = GetCurrentRoomResult(
                current_room=CurrentRoom(
                id=current_room.id,
                exits=exits_in_room,
                description=current_room.description,
                name=current_room.name,
                people=people_in_room
                )
            )
        return output
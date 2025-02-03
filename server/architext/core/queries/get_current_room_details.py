from dataclasses import dataclass
from typing import Literal, List, Optional
from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld, assertUserIsLoggedIn
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.room import Room
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
from architext.core.domain.primitives import Visibility


@dataclass
class PersonInRoomDetails:
    id: str
    name: str

@dataclass
class ExitInRoomDetails:
    name: str
    description: str
    visibility: Visibility
    destination_id: str
    destination_name: str

@dataclass
class CurrentRoomDetails:
    id: str
    name: str
    description: str
    exits: List[ExitInRoomDetails]
    people: List[PersonInRoomDetails]

@dataclass
class GetCurrentRoomDetailsResult:
    current_room: Optional[CurrentRoomDetails]

class GetCurrentRoomDetails(Query[GetCurrentRoomDetailsResult]):
    pass

class GetCurrentRoomDetailsQueryHandler(QueryHandler[GetCurrentRoomDetails, GetCurrentRoomDetailsResult]):
    pass

class UOWGetCurrentRoomDetailsQueryHandler(UOWQueryHandler, GetCurrentRoomDetailsQueryHandler):
    def query(self, query: GetCurrentRoomDetails, client_user_id: str) -> GetCurrentRoomDetailsResult:
        uow = self._uow
        assertUserIsLoggedIn(uow, client_user_id)
        assertUserIsAuthorizedInCurrentWorld(uow, client_user_id)
        user = uow.users.get_user_by_id(client_user_id)
        if user is None:
            raise ValueError("User not found")
        if user.room_id is None:
            output = GetCurrentRoomDetailsResult(current_room=None)
        else:
            current_room = uow.rooms.get_room_by_id(user.room_id)
            if current_room is None:
                raise ValueError("User is not in a room")
            users = uow.users.get_users_in_room(user.room_id)
            people_in_room = [PersonInRoomDetails(id=user.id, name=user.name) for user in users]

            exits_in_room = []
            for exit in current_room.exits:
                destination = uow.rooms.get_room_by_id(exit.destination_room_id)
                if destination is None:
                    continue
                exits_in_room.append(ExitInRoomDetails(
                    name=exit.name, 
                    description=exit.description,
                    visibility=exit.visibility,
                    destination_id=exit.destination_room_id,
                    destination_name=destination.name,
                ))

            output = GetCurrentRoomDetailsResult(
                current_room=CurrentRoomDetails(
                id=current_room.id,
                exits=exits_in_room,
                description=current_room.description,
                name=current_room.name,
                people=people_in_room
                )
            )
        return output
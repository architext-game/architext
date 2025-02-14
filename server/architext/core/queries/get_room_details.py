from dataclasses import dataclass
from typing import Literal, List, Optional

from pydantic import Field
from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld, assertUserIsLoggedIn
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.room import Room
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
from architext.core.domain.primitives import Visibility


@dataclass
class PersonInRoomDetails:
    id: str
    name: str
    active: bool

@dataclass
class ExitInRoomDetails:
    name: str
    description: str
    visibility: Visibility
    destination_id: str
    destination_name: str

@dataclass
class ItemInRoomDetails:
    name: str
    description: str
    visibility: Visibility

@dataclass
class RoomDetails:
    id: str
    world_id: str
    name: str
    description: str
    exits: List[ExitInRoomDetails]
    items: List[ItemInRoomDetails]
    people: List[PersonInRoomDetails]

@dataclass
class GetRoomDetailsResult:
    room: Optional[RoomDetails]

class GetRoomDetails(Query[GetRoomDetailsResult]):
    room_id: Optional[str] = Field(None)

class GetRoomDetailsQueryHandler(QueryHandler[GetRoomDetails, GetRoomDetailsResult]):
    pass

class UOWGetRoomDetailsQueryHandler(UOWQueryHandler, GetRoomDetailsQueryHandler):
    def query(self, query: GetRoomDetails, client_user_id: str) -> GetRoomDetailsResult:
        uow = self._uow
        assertUserIsLoggedIn(uow, client_user_id)
        assertUserIsAuthorizedInCurrentWorld(uow, client_user_id)
        user = uow.users.get_user_by_id(client_user_id)
        if user is None:
            raise ValueError("User not found")
        
        room_id = query.room_id if query.room_id is not None else user.room_id

        if room_id is None:
            output = GetRoomDetailsResult(room=None)
        else:
            room = uow.rooms.get_room_by_id(room_id)
            if room is None:
                return GetRoomDetailsResult(room=None)
            users = uow.users.get_users_in_room(room_id)
            people_in_room = [PersonInRoomDetails(
                id=user.id,
                name=user.name,
                active=user.active,
            ) for user in users]

            exits_in_room = []
            for exit in room.exits.values():
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

            items_in_room = []
            for item in room.items.values():
                items_in_room.append(ItemInRoomDetails(
                    name=item.name, 
                    description=item.description,
                    visibility=item.visibility,
                ))

            output = GetRoomDetailsResult(
                room=RoomDetails(
                    id=room.id,
                    world_id=room.world_id,
                    exits=exits_in_room,
                    items=items_in_room,
                    description=room.description,
                    name=room.name,
                    people=people_in_room
                )
            )
        return output
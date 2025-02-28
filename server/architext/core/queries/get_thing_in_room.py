from dataclasses import dataclass, field
import re
from typing import Literal, List, Optional, Union
import unicodedata
from architext.core.authorization import assertUserIsLoggedIn
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.item import Item
from architext.core.domain.entities.room import Room
from architext.core.domain.names import hidden_name_match, visible_name_match, complete_name_match
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler

@dataclass
class ExitInRoom:
    name: str
    description: str

@dataclass
class ItemInRoom:
    name: str
    description: str

@dataclass
class GetThingInRoomResult:
    status: Literal['item_matched', 'exit_matched', 'none_found', 'multiple_matches']
    item_match: Optional[ItemInRoom] = None
    exit_match: Optional[ExitInRoom] = None
    multiple_matches: List[str] = field(default_factory=list)

class GetThingInRoom(Query[GetThingInRoomResult]):
    partial_name: str
    restrict_to: Optional[Literal['items', 'exits']] = None

class GetThingInRoomQueryHandler(QueryHandler[GetThingInRoom, GetThingInRoomResult]):
    pass

class UOWGetThingInRoomQueryHandler(UOWQueryHandler, GetThingInRoomQueryHandler):
    def query(self, query: GetThingInRoom, client_user_id: str) -> GetThingInRoomResult:
        uow = self._uow
        with uow as transaction:
            assertUserIsLoggedIn(transaction, client_user_id)
            user = transaction.users.get_user_by_id(client_user_id)

            if user is None:
                raise ValueError("User not found")
            if user.room_id is None:
                raise ValueError("User is not in a room")
            current_room = transaction.rooms.get_room_by_id(user.room_id)
            if current_room is None:
                raise ValueError(f"Room with id {user.room_id} not found")

            things: List[Union[Item, Exit]]
            if query.restrict_to == 'exits':
                things = list(current_room.exits.values()) 
            elif query.restrict_to == 'items':
                things = list(current_room.items.values())
            else:
                things = list(current_room.items.values()) + list(current_room.exits.values())
            match = complete_name_match(query.partial_name, things)

            if match:
                item_match = isinstance(match, Item)
                return GetThingInRoomResult(
                    status="item_matched" if item_match else "exit_matched",
                    item_match=match if item_match else None,
                    exit_match=match if not item_match else None,
                )

            matches = visible_name_match(query.partial_name, things)

            if len(matches) > 1:
                return GetThingInRoomResult(
                    status="multiple_matches",
                    multiple_matches=[m.name for m in matches]
                )
            
            if len(matches) == 1:
                match = matches[0]
                item_match = isinstance(match, Item)
                return GetThingInRoomResult(
                    status="item_matched" if item_match else "exit_matched",
                    item_match=match if item_match else None,
                    exit_match=match if not item_match else None,
                )

            matches = hidden_name_match(query.partial_name, things)

            if len(matches) == 1:
                match = matches[0]
                item_match = isinstance(match, Item)
                return GetThingInRoomResult(
                    status="item_matched" if item_match else "exit_matched",
                    item_match=match if item_match else None,
                    exit_match=match if not item_match else None,
                )

            # Nothing matched or many hidden matched
            return GetThingInRoomResult(
                status='none_found'
            )

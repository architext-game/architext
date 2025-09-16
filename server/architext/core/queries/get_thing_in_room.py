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

            matches = current_room.find(query.partial_name)

            if query.restrict_to == "exits":
                matches = [m for m in matches if isinstance(m, Exit)]
            elif query.restrict_to == "items":
                matches = [m for m in matches if isinstance(m, Item)]

            if len(matches) > 1:
                return GetThingInRoomResult(
                    status="multiple_matches",
                    multiple_matches=[m.name for m in matches]
                )
            
            if len(matches) == 0:
                return GetThingInRoomResult(
                    status='none_found'
                )
            
            match = matches[0]

            if isinstance(match, Item):
                return GetThingInRoomResult(
                    status="item_matched",
                    item_match=ItemInRoom(
                        name=match.name,
                        description=match.description
                    ),
                    exit_match=None,
                )
            
            if isinstance(match, Exit):
                return GetThingInRoomResult(
                    status="exit_matched",
                    item_match=None,
                    exit_match=ExitInRoom(
                        name=match.name,
                        description=match.description
                    ),
                )
            
            raise Exception("room.find returned something different from an item or exit.")

from dataclasses import dataclass
from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld, assertUserIsLoggedIn
from architext.core.domain.entities.item import Item
from architext.core.domain.entities.room import DuplicatedNameInRoom
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
from typing import Literal, Optional


@dataclass
class IsNameValidResult:
    is_valid: bool
    error: Optional[Literal['duplicated']]

class IsNameValid(Query[IsNameValidResult]):
    """Check if a name is valid for a new exit or item in the current room."""
    name: str
    in_room_id: str

class IsNameValidQueryHandler(QueryHandler[IsNameValid, IsNameValidResult]):
    pass

class UOWIsNameValidQueryHandler(UOWQueryHandler, IsNameValidQueryHandler):
    def query(self, query: IsNameValid, client_user_id: str) -> IsNameValidResult:
        assertUserIsLoggedIn(self._uow, client_user_id)
        assertUserIsAuthorizedInCurrentWorld(self._uow, client_user_id)

        user = self._uow.users.get_user_by_id(client_user_id)
        if user is None:
            raise Exception(f'User {client_user_id} not found')
        
        room = self._uow.rooms.get_room_by_id(query.in_room_id)
        if room is None:
            raise Exception(f'Room {query.in_room_id} not found')

        error: Optional[Literal['duplicated']]
        try:
            room.with_item(Item(
                name=query.name,
                description="Dummy description",
                visibility='auto'
            ))
            valid = True
            error = None
        except DuplicatedNameInRoom:
            valid = False
            error = 'duplicated'

        print("EXIT NAME", query.name, "IS VALID IN", query.in_room_id, "?", valid)

        return IsNameValidResult(
            is_valid=valid,
            error=error,
        )
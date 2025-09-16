from architext.core.application.authorization import assertUserIsAuthorizedInCurrentWorld, assertUserIsLoggedIn
from architext.core.domain.entities.item import Item
from architext.core.domain.entities.room import DuplicatedNameInRoom
from architext.core.application.queries.base import QueryHandler, UOWQueryHandler
from architext.core.application.queries.is_name_valid.query import IsNameValid, IsNameValidResult
from typing import Literal, Optional


class IsNameValidQueryHandler(QueryHandler[IsNameValid, IsNameValidResult]):
    pass

class UOWIsNameValidQueryHandler(UOWQueryHandler, IsNameValidQueryHandler):
    def query(self, query: IsNameValid, client_user_id: str) -> IsNameValidResult:
        with self._uow as transaction:
            assertUserIsLoggedIn(transaction, client_user_id)
            assertUserIsAuthorizedInCurrentWorld(transaction, client_user_id)

            user = transaction.users.get_user_by_id(client_user_id)
            if user is None:
                raise Exception(f'User {client_user_id} not found')
            
            if query.in_room_id:
                room = transaction.rooms.get_room_by_id(query.in_room_id)
                if room is None:
                    raise Exception(f'Room {query.in_room_id} not found')
            else:
                if user.room_id is None:
                    raise Exception(f'Room is not provided and user is not in a room')
                room = transaction.rooms.get_room_by_id(user.room_id)
                if room is None:
                    raise Exception(f'User\'s room id is invalid: {user.room_id}')
            
            error: Optional[Literal['duplicated']]
            try:
                room.can_add_item(Item(
                    name=query.name,
                    description="Dummy description",
                    visibility='auto'
                ))
                valid = True
                error = None
            except DuplicatedNameInRoom:
                valid = False
                error = 'duplicated'

            return IsNameValidResult(
                is_valid=valid,
                error=error,
            ) 
from architext.core.application.authorization import assertUserIsLoggedIn
from architext.core.application.queries.base import QueryHandler, UOWQueryHandler
from architext.core.application.queries.get_current_room.query import GetCurrentRoom, GetCurrentRoomResult, PersonInRoom, ExitInRoom, ItemInRoom, CurrentRoom


class GetCurrentRoomQueryHandler(QueryHandler[GetCurrentRoom, GetCurrentRoomResult]):
    pass


class UOWGetCurrentRoomQueryHandler(UOWQueryHandler, GetCurrentRoomQueryHandler):
    def query(self, query: GetCurrentRoom, client_user_id: str) -> GetCurrentRoomResult:
        uow = self._uow
        with uow as transaction:
            assertUserIsLoggedIn(transaction, client_user_id)
            user = transaction.users.get_user_by_id(client_user_id)
            if user is None:
                raise ValueError("User not found")
            if user.room_id is None:
                output = GetCurrentRoomResult(current_room=None)
            else:
                current_room = transaction.rooms.get_room_by_id(user.room_id)
                if current_room is None:
                    raise ValueError("User is not in a room")
                users = transaction.users.get_users_in_room(user.room_id)
                people_in_room = [PersonInRoom(id=user.id, name=user.name) for user in users if user.active]
                exits_in_room = [ExitInRoom(
                    name=exit.name, 
                    description=exit.description,
                    list_in_room_description=current_room.should_be_listed(exit_or_item_name=exit.name),
                ) for exit in current_room.exits.values() if exit.visibility != "hidden"]
                items_in_room = [ItemInRoom(
                    name=item.name, 
                    description=item.description,
                    list_in_room_description=current_room.should_be_listed(exit_or_item_name=item.name),
                ) for item in current_room.items.values() if item.visibility != "hidden"]
                output = GetCurrentRoomResult(
                    current_room=CurrentRoom(
                        exits=exits_in_room,
                        items=items_in_room,
                        description=current_room.description,
                        name=current_room.name,
                        people=people_in_room
                    )
                )
            return output 
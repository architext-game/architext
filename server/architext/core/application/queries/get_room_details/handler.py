from architext.core.application.authorization import assertUserIsAuthorizedInCurrentWorld, assertUserIsLoggedIn
from architext.core.application.queries.base import QueryHandler, UOWQueryHandler
from architext.core.application.queries.get_room_details.query import (
    GetRoomDetails,
    GetRoomDetailsResult,
    PersonInRoomDetails,
    ExitInRoomDetails,
    ItemInRoomDetails,
    RoomDetails,
)


class GetRoomDetailsQueryHandler(QueryHandler[GetRoomDetails, GetRoomDetailsResult]):
    pass

class UOWGetRoomDetailsQueryHandler(UOWQueryHandler, GetRoomDetailsQueryHandler):
    def query(self, query: GetRoomDetails, client_user_id: str) -> GetRoomDetailsResult:
        uow = self._uow
        with uow as transaction:
            assertUserIsLoggedIn(transaction, client_user_id)
            assertUserIsAuthorizedInCurrentWorld(transaction, client_user_id)
            user = transaction.users.get_user_by_id(client_user_id)
            if user is None:
                raise ValueError("User not found")
            
            room_id = query.room_id if query.room_id is not None else user.room_id

            if room_id is None:
                output = GetRoomDetailsResult(room=None)
            else:
                room = transaction.rooms.get_room_by_id(room_id)
                if room is None:
                    return GetRoomDetailsResult(room=None)
                users = transaction.users.get_users_in_room(room_id)
                people_in_room = [PersonInRoomDetails(
                    id=user.id,
                    name=user.name,
                    active=user.active,
                ) for user in users]

                exits_in_room = []
                for exit in room.exits.values():
                    destination = transaction.rooms.get_room_by_id(exit.destination_room_id)
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
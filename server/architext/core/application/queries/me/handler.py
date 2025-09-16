from dataclasses import dataclass
from typing import Optional
from architext.core.application.queries.base import Query, QueryHandler, UOWQueryHandler
from architext.core.application.queries.me.query import Me, MeResult, UserNotFound

class MeQueryHandler(QueryHandler[Me, MeResult]):
    pass

class UOWMeQueryHandler(UOWQueryHandler, MeQueryHandler):
    def query(self, query: Me, client_user_id: str) -> MeResult:
        with self._uow as transaction:
            world = None
            if client_user_id is None:
                raise Exception('No user id provided')
            user = transaction.users.get_user_by_id(client_user_id)
            if user is None:
                raise UserNotFound(f'User {client_user_id} not found')
            world_id = None
            if user.room_id:
                room = transaction.rooms.get_room_by_id(user.room_id)
                assert room is not None
                world_id = room.world_id
                world = transaction.worlds.get_world_by_id(world_id)
            
            return MeResult(
                name=user.name,
                email=user.email or '',
                current_world_id=world_id,
                id=user.id,
                privileged_in_current_world=world is not None and world.owner_user_id == user.id,
            )


from dataclasses import dataclass
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
from typing import Literal, Optional

@dataclass
class GetWorldResult:
    id: str
    name: str
    description: str
    owner_name: Optional[str]
    connected_players_count: int
    base_template_name: Optional[str]
    base_template_author: Optional[str]
    visibility: Literal["public", "private"]
    you_authorized: bool

class GetWorld(Query[GetWorldResult]):
    world_id: str

class GetWorldQueryHandler(QueryHandler[GetWorld, GetWorldResult]):
    pass

class UOWGetWorldQueryHandler(UOWQueryHandler, GetWorldQueryHandler):
    def query(self, query: GetWorld, client_user_id: str) -> GetWorldResult:
        with self._uow as transaction:
            user = transaction.users.get_user_by_id(client_user_id)
            if user is None:
                raise Exception(f'User {client_user_id} not found')
            world = transaction.worlds.get_world_by_id(query.world_id)
            if world is None:
                raise Exception(f'World {query.world_id} not found')

            users = transaction.users.list_users()
            room_ids = [room.id for room in transaction.rooms.list_rooms_by_world(world.id)]
            players_in_world = [user for user in users if user.room_id in room_ids and user.active]

            template = transaction.world_templates.get_world_template_by_id(world.base_template_id) if world.base_template_id is not None else None

            owner = transaction.users.get_user_by_id(world.owner_user_id) if world.owner_user_id is not None else None

            return GetWorldResult(
                id=world.id,
                name=world.name,
                description=world.description,
                owner_name=owner.name if owner is not None else None,
                connected_players_count=len(players_in_world),
                base_template_name=template.name if template is not None else None,
                base_template_author=template.author_id if template is not None else None,
                visibility=world.visibility,
                you_authorized=world.owner_user_id == client_user_id,
            )
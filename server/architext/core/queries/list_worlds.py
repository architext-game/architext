from dataclasses import dataclass
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
from typing import Literal, Optional, List

@dataclass
class WorldListItem:
    id: str
    name: str
    description: str
    owner_name: Optional[str]
    connected_players_count: int
    base_template_name: Optional[str]
    base_template_author: Optional[str]
    visibility: Literal["public", "private"]

@dataclass
class ListWorldsResult:
    worlds: List[WorldListItem]

class ListWorlds(Query[ListWorldsResult]):
    pass

class ListWorldsQueryHandler(QueryHandler[ListWorlds, ListWorldsResult]):
    pass

class UOWListWorldsQueryHandler(UOWQueryHandler, ListWorldsQueryHandler):
    def query(self, query: ListWorlds, client_user_id: str) -> ListWorldsResult:
        user = self._uow.users.get_user_by_id(client_user_id)
        if user is None:
            raise Exception(f'User {client_user_id} not found')
        worlds = ([
            world
            for world in self._uow.worlds.list_worlds()
            if world.visibility == "public" 
            or world.owner_user_id == client_user_id 
            or world.id in user.visited_world_ids
        ])
        result: List[WorldListItem] = []
        for world in worlds:
            owner = self._uow.users.get_user_by_id(world.owner_user_id) if world.owner_user_id is not None else None
            template = self._uow.world_templates.get_world_template_by_id(world.base_template_id) if world.base_template_id is not None else None
            users = self._uow.users.list_users()
            room_ids = [room.id for room in self._uow.rooms.list_rooms_by_world(world.id)]
            players_in_world = [user for user in users if user.room_id in room_ids]
            result.append(WorldListItem(
                id=world.id,
                description=world.description,
                name=world.name,
                owner_name=owner.name if owner is not None else "Architext",
                connected_players_count=len(players_in_world),
                base_template_name=template.name if template is not None else None,
                base_template_author=template.author_id if template is not None else None,
                visibility=world.visibility,
            ))
            
        return ListWorldsResult(worlds=result)
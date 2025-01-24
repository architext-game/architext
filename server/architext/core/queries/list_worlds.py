from dataclasses import dataclass
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
from typing import Optional, List

@dataclass
class WorldListItem:
    id: str
    name: str
    description: str
    owner: Optional[str]

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
        return ListWorldsResult(worlds=[WorldListItem(
            id=world.id,
            description=world.description,
            name=world.name,
            owner=world.owner_user_id
        ) for world in self._uow.worlds.list_worlds()
            if world.visibility == "public" 
            or world.owner_user_id == client_user_id 
            or world.id in user.visited_world_ids
        ])
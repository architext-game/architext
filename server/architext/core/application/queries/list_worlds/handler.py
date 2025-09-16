from typing import List
from architext.core.application.queries.base import QueryHandler, UOWQueryHandler
from architext.core.application.queries.list_worlds.query import ListWorlds, ListWorldsResult, WorldListItem


class ListWorldsQueryHandler(QueryHandler[ListWorlds, ListWorldsResult]):
    pass

class UOWListWorldsQueryHandler(UOWQueryHandler, ListWorldsQueryHandler):
    def query(self, query: ListWorlds, client_user_id: str) -> ListWorldsResult:
        with self._uow as transaction:
            user = transaction.users.get_user_by_id(client_user_id)
            if user is None:
                raise Exception(f'User {client_user_id} not found')
            worlds = ([
                world
                for world in transaction.worlds.list_worlds()
                if world.visibility == "public" 
                or world.owner_user_id == client_user_id 
                or world.id in user.visited_world_ids
            ])
            result: List[WorldListItem] = []
            for world in worlds:
                owner = transaction.users.get_user_by_id(world.owner_user_id) if world.owner_user_id is not None else None
                template = transaction.world_templates.get_world_template_by_id(world.base_template_id) if world.base_template_id is not None else None
                users = transaction.users.list_users()
                room_ids = [room.id for room in transaction.rooms.list_rooms_by_world(world.id)]
                players_in_world = [user for user in users if user.room_id in room_ids and user.active]
                result.append(WorldListItem(
                    id=world.id,
                    description=world.description,
                    name=world.name,
                    owner_name=owner.name if owner is not None else "Architext",
                    connected_players_count=len(players_in_world),
                    base_template_name=template.name if template is not None else None,
                    base_template_author=template.author_id if template is not None else None,
                    visibility=world.visibility,
                    you_authorized=world.owner_user_id == client_user_id,
                ))
                
            return ListWorldsResult(worlds=result) 
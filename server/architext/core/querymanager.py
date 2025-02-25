
from typing import Type, TypeVar, Mapping, TYPE_CHECKING
from architext.core.queries.available_missions import AvailableMissions, UOWAvailableMissionsQueryHandler
from architext.core.queries.base import Query, QueryHandler
from architext.core.queries.get_current_room import GetCurrentRoom, UOWGetCurrentRoomQueryHandler
from architext.core.queries.get_room_details import GetRoomDetails, UOWGetRoomDetailsQueryHandler
from architext.core.queries.get_template import GetWorldTemplate, UOWGetWorldTemplateQueryHandler
from architext.core.queries.get_thing_in_room import GetThingInRoom, UOWGetThingInRoomQueryHandler
from architext.core.queries.is_name_valid import IsNameValid, UOWIsNameValidQueryHandler
from architext.core.queries.list_world_templates import UOWListWorldTemplatesQueryHandler, ListWorldTemplates
from architext.core.queries.list_worlds import ListWorlds, UOWListWorldsQueryHandler
from architext.core.queries.me import Me, UOWMeQueryHandler
from architext.core.queries.get_world import GetWorld, UOWGetWorldQueryHandler
from architext.core.queries.world_to_text import WorldToText, UOWWorldToTextQueryHandler
if TYPE_CHECKING:
    from architext.core.ports.unit_of_work import UnitOfWork
else:
    UnitOfWork = object()

T = TypeVar('T')

def uow_query_handlers_factory(uow: UnitOfWork) -> Mapping[Type[Query], QueryHandler]:
    return {
        ListWorlds: UOWListWorldsQueryHandler(uow),
        WorldToText: UOWWorldToTextQueryHandler(uow),
        ListWorldTemplates: UOWListWorldTemplatesQueryHandler(uow),
        Me: UOWMeQueryHandler(uow),
        GetWorldTemplate: UOWGetWorldTemplateQueryHandler(uow),
        GetWorld: UOWGetWorldQueryHandler(uow),
        GetCurrentRoom: UOWGetCurrentRoomQueryHandler(uow),
        GetRoomDetails: UOWGetRoomDetailsQueryHandler(uow),
        IsNameValid: UOWIsNameValidQueryHandler(uow),
        GetThingInRoom: UOWGetThingInRoomQueryHandler(uow),
        AvailableMissions: UOWAvailableMissionsQueryHandler(uow),
    }

class QueryManager:
    def __init__(
            self,
            query_handlers: Mapping[Type[Query], QueryHandler],
        ):
        self._query_handlers = query_handlers

    def query(self, query: Query[T], client_user_id: str = "") -> T:
        return self._query_handlers[type(query)].query(query, client_user_id)

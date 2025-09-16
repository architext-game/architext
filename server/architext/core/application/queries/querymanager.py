"""
This module defines the QueryManager class, which is used to handle queries
and return their results.
"""

from typing import Type, TypeVar, Mapping, TYPE_CHECKING
from architext.core.application.queries.available_missions import AvailableMissions, UOWAvailableMissionsQueryHandler
from architext.core.application.queries.base import Query, QueryHandler
from architext.core.application.queries.get_current_room import GetCurrentRoom, UOWGetCurrentRoomQueryHandler
from architext.core.application.queries.get_room_details import GetRoomDetails, UOWGetRoomDetailsQueryHandler
from architext.core.application.queries.get_template import GetWorldTemplate, UOWGetWorldTemplateQueryHandler
from architext.core.application.queries.get_thing_in_room import GetThingInRoom, UOWGetThingInRoomQueryHandler
from architext.core.application.queries.is_name_valid import IsNameValid, UOWIsNameValidQueryHandler
from architext.core.application.queries.list_world_templates import UOWListWorldTemplatesQueryHandler, ListWorldTemplates
from architext.core.application.queries.list_worlds import ListWorlds, UOWListWorldsQueryHandler
from architext.core.application.queries.me import Me, UOWMeQueryHandler
from architext.core.application.queries.get_world import GetWorld, UOWGetWorldQueryHandler
from architext.core.application.queries.world_to_text import WorldToText, UOWWorldToTextQueryHandler
if TYPE_CHECKING:
    from architext.core.application.ports.unit_of_work import UnitOfWork
else:
    UnitOfWork = object()

T = TypeVar('T')

# At the moment every query handler uses the UOW to access the data
# through the repositories.
# In the future I plan to make raw SQL queries versions of queries that
# need to be optimized.
def uow_query_handlers_factory(uow: UnitOfWork) -> Mapping[Type[Query], QueryHandler]:
    """
    Factory method used to create a mapping of query types to query handlers,
    injecting a UnitOfWork into every handler.
    """
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
        """
        Receives a query and returns its result.
        """
        return self._query_handlers[type(query)].query(query, client_user_id)

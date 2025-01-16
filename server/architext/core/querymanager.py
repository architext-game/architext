
from typing import Type, TypeVar, Mapping
from architext.core.queries.base import Query, QueryHandler
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.queries.list_worlds import ListWorlds, UOWListWorldsQueryHandler

T = TypeVar('T')

def uow_query_handlers_factory(uow: UnitOfWork) -> Mapping[Type[Query], QueryHandler]:
    return {
        ListWorlds: UOWListWorldsQueryHandler(uow)
    }

class QueryManager:
    def __init__(
            self,
            query_handlers: Mapping[Type[Query], QueryHandler],
        ):
        self._query_handlers = query_handlers

    def query(self, query: Query[T], client_user_id: str = "") -> T:
        return self._query_handlers[type(query)].query(query, client_user_id)

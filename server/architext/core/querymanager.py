from typing import List, Dict, Callable, Type, TypeVar, Union, Any, Mapping
from architext.core.domain.events import Event
from architext.core.commands import Command
from architext.core.queries import Query, QueryHandler
import logging
from architext.core.ports.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)

Message = Union[Event, Command]

T = TypeVar("T")

class QueryManager:
    def __init__(
            self,
            query_handlers: Mapping[Type[Query], QueryHandler],
        ):
        self._query_handlers = query_handlers

    def query(self, uow: UnitOfWork, query: Query[T], client_user_id: str = "") -> T:
        return self._query_handlers[type(query)].query(query, client_user_id)

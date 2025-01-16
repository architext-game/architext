

from typing import TypeVar
from architext.core.commands import Command
from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.queries.base import Query
from architext.core.querymanager import QueryManager, uow_query_handlers_factory

T = TypeVar("T")

class Architext:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
        self._messagebus = MessageBus()
        self._queryhandler = QueryManager(query_handlers=uow_query_handlers_factory(uow))

    def handle(self, command: Command[T], client_user_id: str = "") -> T:
        return self._messagebus.handle(self._uow, command, client_user_id)

    def query(self, query: Query[T], client_user_id: str = "") -> T:
        return self._queryhandler.query(query, client_user_id)
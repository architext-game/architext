from typing import Dict, List, Optional, Protocol, Type, TypeVar, Generic, Mapping
from pydantic import BaseModel, Field, EmailStr
from dataclasses import dataclass

from architext.core.ports.unit_of_work import UnitOfWork

T = TypeVar('T', contravariant=True)
K = TypeVar('K', covariant=True)

class Query(BaseModel, Generic[T]):
    pass

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

class QueryHandler(Protocol, Generic[T, K]):
    def query(self, query: T, client_user_id: str) -> K:
        pass

class UOWQueryHandler(QueryHandler):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

class ListWorldsQueryHandler(QueryHandler[ListWorlds, ListWorldsResult]):
    pass

class UOWListWorldsQueryHandler(UOWQueryHandler, ListWorldsQueryHandler):
    def query(self, query: ListWorlds, client_user_id: str) -> ListWorldsResult:
        return ListWorldsResult(worlds=[WorldListItem(
            id=world.id,
            description=world.description,
            name=world.name,
            owner=world.owner_user_id
        ) for world in self._uow.worlds.list_worlds()])

def uow_query_handlers_factory(uow: UnitOfWork) -> Mapping[Type[Query], QueryHandler]:
    return {
        ListWorlds: UOWListWorldsQueryHandler(uow)
    }

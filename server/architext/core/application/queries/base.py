
from typing import Protocol, TypeVar, Generic
from pydantic import BaseModel
from typing import TypeVar, TYPE_CHECKING
if TYPE_CHECKING:
    from architext.core.application.ports.unit_of_work import UnitOfWork
else:
    UnitOfWork = object()


T = TypeVar('T', contravariant=True)
K = TypeVar('K', covariant=True)

class Query(BaseModel, Generic[T]):
    ...

class QueryHandler(Protocol, Generic[T, K]):
    def query(self, query: T, client_user_id: str) -> K:
        ...

class UOWQueryHandler(QueryHandler):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
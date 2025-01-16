
from typing import Dict, List, Optional, Protocol, Type, TypeVar, Generic, Mapping
from pydantic import BaseModel, Field, EmailStr
from dataclasses import dataclass
from typing import List, Dict, Callable, Type, TypeVar, Union, Any, Mapping
from architext.core.domain.events import Event
from architext.core.commands import Command
import logging
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.ports.unit_of_work import UnitOfWork


T = TypeVar('T', contravariant=True)
K = TypeVar('K', covariant=True)

class Query(BaseModel, Generic[T]):
    pass

class QueryHandler(Protocol, Generic[T, K]):
    def query(self, query: T, client_user_id: str) -> K:
        pass

class UOWQueryHandler(QueryHandler):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
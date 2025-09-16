from dataclasses import dataclass
from typing import Optional
from architext.core.application.queries.base import Query, QueryHandler, UOWQueryHandler

@dataclass
class MeResult:
    name: str
    email: str
    current_world_id: Optional[str]
    privileged_in_current_world: bool
    id: str

class Me(Query[MeResult]):
    pass

class UserNotFound(Exception):
    pass
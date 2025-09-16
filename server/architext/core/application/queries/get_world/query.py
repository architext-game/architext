from dataclasses import dataclass
from architext.core.application.queries.base import Query
from typing import Literal, Optional


@dataclass
class GetWorldResult:
    id: str
    name: str
    description: str
    owner_name: Optional[str]
    connected_players_count: int
    base_template_name: Optional[str]
    base_template_author: Optional[str]
    visibility: Literal["public", "private"]
    you_authorized: bool

class GetWorld(Query[GetWorldResult]):
    world_id: str 
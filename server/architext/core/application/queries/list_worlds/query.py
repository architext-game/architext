from dataclasses import dataclass
from architext.core.application.queries.base import Query
from typing import Literal, Optional, List


@dataclass
class WorldListItem:
    id: str
    name: str
    description: str
    owner_name: Optional[str]
    connected_players_count: int
    base_template_name: Optional[str]
    base_template_author: Optional[str]
    visibility: Literal["public", "private"]
    you_authorized: bool

@dataclass
class ListWorldsResult:
    worlds: List[WorldListItem]

class ListWorlds(Query[ListWorldsResult]):
    pass 
from dataclasses import dataclass, field
from typing import Literal, List, Optional, Union
from architext.core.application.queries.base import Query


@dataclass
class ExitInRoom:
    name: str
    description: str

@dataclass
class ItemInRoom:
    name: str
    description: str

@dataclass
class GetThingInRoomResult:
    status: Literal['item_matched', 'exit_matched', 'none_found', 'multiple_matches']
    item_match: Optional[ItemInRoom] = None
    exit_match: Optional[ExitInRoom] = None
    multiple_matches: List[str] = field(default_factory=list)

class GetThingInRoom(Query[GetThingInRoomResult]):
    partial_name: str
    restrict_to: Optional[Literal['items', 'exits']] = None 
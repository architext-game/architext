from dataclasses import dataclass
from typing import Literal, List, Optional, Union
from architext.core.application.queries.base import Query


@dataclass
class PersonInRoom:
    id: str
    name: str

@dataclass
class ExitInRoom:
    name: str
    description: str
    list_in_room_description: bool

@dataclass
class ItemInRoom:
    name: str
    description: str
    list_in_room_description: bool

@dataclass
class CurrentRoom:
    name: str
    description: str
    exits: List[ExitInRoom]
    items: List[ItemInRoom]
    people: List[PersonInRoom]

@dataclass
class GetCurrentRoomResult:
    current_room: Optional[CurrentRoom]

class GetCurrentRoom(Query[GetCurrentRoomResult]):
    pass 
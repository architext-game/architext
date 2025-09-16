from dataclasses import dataclass
from typing import Literal, List, Optional
from pydantic import Field
from architext.core.application.queries.base import Query
from architext.core.domain.primitives import Visibility


@dataclass
class PersonInRoomDetails:
    id: str
    name: str
    active: bool

@dataclass
class ExitInRoomDetails:
    name: str
    description: str
    visibility: Visibility
    destination_id: str
    destination_name: str

@dataclass
class ItemInRoomDetails:
    name: str
    description: str
    visibility: Visibility

@dataclass
class RoomDetails:
    id: str
    world_id: str
    name: str
    description: str
    exits: List[ExitInRoomDetails]
    items: List[ItemInRoomDetails]
    people: List[PersonInRoomDetails]

@dataclass
class GetRoomDetailsResult:
    room: Optional[RoomDetails]

class GetRoomDetails(Query[GetRoomDetailsResult]):
    room_id: Optional[str] = Field(None) 
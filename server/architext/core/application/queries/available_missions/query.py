from dataclasses import dataclass
from typing import List
from architext.core.application.authorization import assertUserIsLoggedIn
from architext.core.domain.entities.mission import is_mission_available
from architext.core.application.queries.base import Query, QueryHandler, UOWQueryHandler

@dataclass
class AvailableMission:
    id: str
    name: str
    description: str

@dataclass
class AvailableMissionsResult:
    missions: List[AvailableMission]

class AvailableMissions(Query[AvailableMissionsResult]):
    pass
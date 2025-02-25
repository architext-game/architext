from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, List, Optional, Union
from architext.core.authorization import assertUserIsLoggedIn
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.item import Item
from architext.core.domain.entities.room import Room
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
if TYPE_CHECKING:
    from architext.core.ports.unit_of_work import UnitOfWork
else:
    UnitOfWork = object()

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

class AvailableMissionsQueryHandler(QueryHandler[AvailableMissions, AvailableMissionsResult]):
    pass

def should_be_listed(exit: Union[Item, Exit], room: Room) -> bool:
    if exit.visibility == "auto":
        if exit.name.lower() in room.description.lower():
            return False
        else:
            return True
    elif exit.visibility == "unlisted":
        return False
    elif exit.visibility == "listed":
        return True
    else:  # exit is hidden, this won't be in the query results
        return False  

def is_mission_completed(uow: UnitOfWork, mission_id: str, user_id: str):
    log = uow.missions.get_mission_log(mission_id=mission_id, user_id=user_id)
    return log is not None and log.completed_at is not None

def is_mission_available(uow: UnitOfWork, mission_id: str, user_id: str):
    mission = uow.missions.get_mission_by_id(mission_id=mission_id)
    if mission is None:
        return False
    
    if is_mission_completed(uow=uow, mission_id=mission_id, user_id=user_id):
        return False

    for required_mission in mission.requirements:
        log = uow.missions.get_mission_log(mission_id=required_mission.complete_mission_with_id, user_id=user_id)
        if log is None or log.completed_at is None:
            return False
    
    return True

class UOWAvailableMissionsQueryHandler(UOWQueryHandler, AvailableMissionsQueryHandler):
    def query(self, query: AvailableMissions, client_user_id: str) -> AvailableMissionsResult:
        uow = self._uow
        with uow:
            assertUserIsLoggedIn(uow, client_user_id)
            user = uow.users.get_user_by_id(client_user_id)
            if user is None:
                raise ValueError("User not found")
            missions = uow.missions.list_missions()
            logs = uow.missions.list_mission_logs_by_user_id(user_id=client_user_id)
            completed_ids = [log.mission_id for log in logs if log.completed_at is not None]

            available_missions = [
                AvailableMission(
                    id=mission.id,
                    name=mission.name,
                    description=mission.description
                ) for mission in missions if is_mission_available(
                    uow=uow,
                    mission_id=mission.id,
                    user_id=client_user_id
                )
            ]

        return AvailableMissionsResult(missions=available_missions)
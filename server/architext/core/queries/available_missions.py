from dataclasses import dataclass
from typing import List
from architext.core.authorization import assertUserIsLoggedIn
from architext.core.domain.entities.mission import is_mission_available
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler

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

class UOWAvailableMissionsQueryHandler(UOWQueryHandler, AvailableMissionsQueryHandler):
    def query(self, query: AvailableMissions, client_user_id: str) -> AvailableMissionsResult:
        uow = self._uow
        with uow as transaction:
            assertUserIsLoggedIn(transaction, client_user_id)
            user = transaction.users.get_user_by_id(client_user_id)
            if user is None:
                raise ValueError("User not found")
            missions = transaction.missions.list_missions()
            logs = transaction.missions.list_mission_logs_by_user_id(user_id=client_user_id)
            completed_ids = [log.mission_id for log in logs if log.completed_at is not None]

            available_missions = [
                AvailableMission(
                    id=mission.id,
                    name=mission.name,
                    description=mission.description
                ) for mission in missions if is_mission_available(
                    mission=mission,
                    user_mission_logs=logs,
                )
            ]

        return AvailableMissionsResult(missions=available_missions)
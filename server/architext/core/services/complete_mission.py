from architext.core.commands import CompleteMission, CompleteMissionResult
from architext.core.domain.entities.mission import MissionLog
from architext.core.ports.unit_of_work import UnitOfWork
from datetime import datetime

from architext.core.queries.available_missions import is_mission_available

class MissionUnavailable(Exception):
    pass

def complete_mission(uow: UnitOfWork, command: CompleteMission, client_user_id: str = "") -> CompleteMissionResult:
    with uow:
        user = uow.users.get_user_by_id(user_id=client_user_id)
        if not user:
            raise PermissionError("User does not exist.")
        
        mission = uow.missions.get_mission_by_id(mission_id=command.mission_id)
        if not mission:
            raise MissionUnavailable()
        
        if not is_mission_available(uow=uow, mission_id=command.mission_id, user_id=client_user_id):
            raise MissionUnavailable()
        
        uow.missions.save_mission_log(MissionLog(
            mission_id=command.mission_id,
            user_id=client_user_id,
            completed_at=datetime.now()
        ))
        uow.commit()

    return CompleteMissionResult()

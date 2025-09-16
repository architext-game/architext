from architext.core.commands import CompleteMission, CompleteMissionResult
from architext.core.domain.entities.mission import MissionLog, is_mission_available
from architext.core.ports.unit_of_work import UnitOfWork
from datetime import datetime

class MissionUnavailable(Exception):
    pass

def complete_mission(uow: UnitOfWork, command: CompleteMission, client_user_id: str = "") -> CompleteMissionResult:
    with uow as transaction:
        user = transaction.users.get_user_by_id(user_id=client_user_id)
        if not user:
            raise PermissionError("User does not exist.")
        
        mission = transaction.missions.get_mission_by_id(mission_id=command.mission_id)
        logs = transaction.missions.list_mission_logs_by_user_id(user_id=client_user_id)
        if not mission:
            raise MissionUnavailable()
        
        if not is_mission_available(mission=mission, user_mission_logs=logs):
            raise MissionUnavailable()
        
        transaction.missions.save_mission_log(MissionLog(
            mission_id=command.mission_id,
            user_id=client_user_id,
            completed_at=datetime.now()
        ))

    return CompleteMissionResult()

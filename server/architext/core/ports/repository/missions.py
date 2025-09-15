from typing import Protocol, List, Optional
from architext.core.domain.entities.mission import Mission, MissionLog


class MissionRepository(Protocol):
    def get_mission_by_id(self, mission_id: str) -> Optional[Mission]:
        ...

    def save_mission(self, mission: Mission) -> None:
        ...

    def list_missions(self) -> List[Mission]:
        ...

    def get_mission_log(self, mission_id: str, user_id: str) -> Optional[MissionLog]:
        ...

    def list_mission_logs_by_user_id(self, user_id: str) -> List[MissionLog]:
        ...

    def save_mission_log(self, mission_log: MissionLog):
        ...
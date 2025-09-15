from typing import Dict, List, Optional
from collections import defaultdict
from architext.core.domain.entities.mission import Mission, MissionLog
from architext.core.ports.repository.missions import MissionRepository
from copy import deepcopy


class MemoryMissionRepository(MissionRepository):
    def __init__(self) -> None:
        self._missions: Dict[str, Mission] = {}
        self._logs: Dict[str, Dict[str, MissionLog]] = defaultdict(dict)

    def get_mission_by_id(self, mission_id: str) -> Optional[Mission]:
        mission = self._missions.get(mission_id)
        return deepcopy(mission) if mission else None

    def save_mission(self, mission: Mission) -> None:
        self._missions[mission.id] = deepcopy(mission)

    def list_missions(self) -> List[Mission]:
        return [deepcopy(mission) for mission in self._missions.values()]

    def get_mission_log(self, mission_id: str, user_id: str) -> Optional[MissionLog]:
        mission_log = self._logs.get(mission_id, {}).get(user_id)
        return deepcopy(mission_log) if mission_log else None

    def list_mission_logs_by_user_id(self, user_id: str) -> List[MissionLog]:
        user_logs = []
        for mission_logs in self._logs.values():
            if user_id in mission_logs:
                user_logs.append(deepcopy(mission_logs[user_id]))
        return user_logs

    def save_mission_log(self, mission_log: MissionLog) -> None:
        self._logs[mission_log.mission_id][mission_log.user_id] = deepcopy(mission_log)

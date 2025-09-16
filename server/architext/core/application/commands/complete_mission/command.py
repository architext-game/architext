from dataclasses import dataclass
from architext.core.application.commands.base import Command

@dataclass
class CompleteMissionResult:
    pass

class CompleteMission(Command[CompleteMissionResult]):
    mission_id: str

class MissionUnavailable(Exception):
    pass
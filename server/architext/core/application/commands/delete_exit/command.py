from dataclasses import dataclass
from architext.core.application.commands.base import Command


@dataclass
class DeleteExitResult:
    pass

class DeleteExit(Command[DeleteExitResult]):
    room_id: str
    exit_name: str 
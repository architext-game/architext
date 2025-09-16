from dataclasses import dataclass
from architext.core.application.commands.base import Command


@dataclass
class TraverseExitResult:
    new_room_id: str

class TraverseExit(Command[TraverseExitResult]):
    exit_name: str 
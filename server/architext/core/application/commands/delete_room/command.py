from dataclasses import dataclass
from architext.core.application.commands.base import Command


@dataclass
class DeleteRoomResult:
    pass

class DeleteRoom(Command[DeleteRoomResult]):
    pass 
from dataclasses import dataclass
from architext.core.application.commands.base import Command


@dataclass
class EnterWorldResult:
    pass

class EnterWorld(Command[EnterWorldResult]):
    world_id: str 
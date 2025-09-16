from dataclasses import dataclass
from architext.core.application.commands.base import Command


@dataclass
class DeleteWorldResult:
    pass

class DeleteWorld(Command[DeleteWorldResult]):
    world_id: str 
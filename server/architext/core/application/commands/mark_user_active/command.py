from dataclasses import dataclass
from architext.core.application.commands.base import Command


@dataclass
class MarkUserActiveResult:
    pass

class MarkUserActive(Command[MarkUserActiveResult]):
    active: bool 
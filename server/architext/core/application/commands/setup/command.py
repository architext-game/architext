from dataclasses import dataclass
from architext.core.application.commands.base import Command


@dataclass
class SetupResult:
    pass

class Setup(Command[SetupResult]):
    pass 
from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from architext.core.domain.primitives import Visibility
from architext.core.application.settings import EXIT_NAME_MAX_LENGTH, EXIT_DESCRIPTION_MAX_LENGTH


@dataclass
class CreateExitResult:
    pass

class CreateExit(Command[CreateExitResult]):
    in_room_id: str
    name: str = Field(min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=EXIT_DESCRIPTION_MAX_LENGTH)
    destination_room_id: str = Field(min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    visibility: Visibility 
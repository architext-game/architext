from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from typing import Optional
from architext.core.application.settings import EXIT_NAME_MAX_LENGTH, EXIT_DESCRIPTION_MAX_LENGTH
from architext.core.domain.primitives import Visibility


@dataclass
class EditExitResult:
    pass

class EditExit(Command[EditExitResult]):
    room_id: str
    exit_name: str
    new_name: Optional[str] = Field(None, min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    new_description: Optional[str] = Field(None, min_length=1, max_length=EXIT_DESCRIPTION_MAX_LENGTH)
    new_destination: Optional[str] = Field(None)
    new_visibility: Optional[Visibility] = Field(None) 
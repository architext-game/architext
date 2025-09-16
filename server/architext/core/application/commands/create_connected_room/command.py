from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from architext.core.application.settings import ROOM_NAME_MAX_LENGTH, ROOM_DESCRIPTION_MAX_LENGTH, EXIT_NAME_MAX_LENGTH, EXIT_DESCRIPTION_MAX_LENGTH


@dataclass
class CreateConnectedRoomResult:
    room_id: str

class CreateConnectedRoom(Command[CreateConnectedRoomResult]):
    name: str = Field(min_length=1, max_length=ROOM_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=ROOM_DESCRIPTION_MAX_LENGTH)
    exit_to_new_room_name: str = Field(min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    exit_to_new_room_description: str = Field(min_length=1, max_length=EXIT_DESCRIPTION_MAX_LENGTH)
    exit_to_old_room_name: str = Field(min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    exit_to_old_room_description: str = Field(min_length=1, max_length=EXIT_DESCRIPTION_MAX_LENGTH) 
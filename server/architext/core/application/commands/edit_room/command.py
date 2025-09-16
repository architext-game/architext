from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from typing import Optional
from architext.core.application.settings import ROOM_NAME_MAX_LENGTH, ROOM_DESCRIPTION_MAX_LENGTH


@dataclass
class EditRoomResult:
    pass

class EditRoom(Command[EditRoomResult]):
    room_id: str
    new_name: Optional[str] = Field(None, min_length=1, max_length=ROOM_NAME_MAX_LENGTH)
    new_description: Optional[str] = Field(None, min_length=1, max_length=ROOM_DESCRIPTION_MAX_LENGTH) 
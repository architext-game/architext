from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from typing import Optional
from architext.core.application.settings import USER_NAME_MAX_LENGTH


@dataclass
class UpdateUserSettingsResult:
    pass

class UpdateUserSettings(Command[UpdateUserSettingsResult]):
    new_name: Optional[str] = Field(min_length=1, max_length=USER_NAME_MAX_LENGTH)


class NameAlreadyTaken(Exception):
    def __init__(self, message="Name not available."):
        super().__init__(message) 
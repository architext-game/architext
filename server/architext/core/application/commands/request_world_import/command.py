from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from typing import Literal
from architext.core.application.settings import WORLD_NAME_MAX_LENGTH, WORLD_DESCRIPTION_MAX_LENGTH


@dataclass
class RequestWorldImportResult:
    future_world_id: str

class RequestWorldImport(Command[RequestWorldImportResult]):
    name: str = Field(min_length=1, max_length=WORLD_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=WORLD_DESCRIPTION_MAX_LENGTH)
    format: Literal["plain", "encoded"]
    text_representation: str 
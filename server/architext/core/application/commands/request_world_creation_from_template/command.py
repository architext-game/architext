from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from architext.core.application.settings import WORLD_NAME_MAX_LENGTH, WORLD_DESCRIPTION_MAX_LENGTH


@dataclass
class RequestWorldCreationFromTemplateResult:
    future_world_id: str

class RequestWorldCreationFromTemplate(Command[RequestWorldCreationFromTemplateResult]):
    name: str = Field(min_length=1, max_length=WORLD_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=WORLD_DESCRIPTION_MAX_LENGTH)
    template_id: str 
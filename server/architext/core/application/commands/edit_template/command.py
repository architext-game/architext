from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from typing import Optional
from architext.core.application.settings import WORLD_NAME_MAX_LENGTH, WORLD_DESCRIPTION_MAX_LENGTH


@dataclass
class EditTemplateResult:
    pass

class EditTemplate(Command[EditTemplateResult]):
    template_id: str
    name: Optional[str] = Field(min_length=1, max_length=WORLD_NAME_MAX_LENGTH)
    description: Optional[str] = Field(min_length=1, max_length=WORLD_DESCRIPTION_MAX_LENGTH) 
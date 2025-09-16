from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from typing import Optional
from architext.core.application.settings import ITEM_NAME_MAX_LENGTH, ITEM_DESCRIPTION_MAX_LENGTH
from architext.core.domain.primitives import Visibility


@dataclass
class EditItemResult:
    pass

class EditItem(Command[EditItemResult]):
    room_id: str
    item_name: str
    new_name: Optional[str] = Field(None, min_length=1, max_length=ITEM_NAME_MAX_LENGTH)
    new_description: Optional[str] = Field(None, min_length=1, max_length=ITEM_DESCRIPTION_MAX_LENGTH)
    new_visibility: Optional[Visibility] = Field(None) 
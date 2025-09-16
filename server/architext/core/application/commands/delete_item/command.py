from dataclasses import dataclass
from architext.core.application.commands.base import Command


@dataclass
class DeleteItemResult:
    pass

class DeleteItem(Command[DeleteItemResult]):
    room_id: str
    item_name: str 
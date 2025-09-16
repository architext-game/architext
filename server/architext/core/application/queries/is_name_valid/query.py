from dataclasses import dataclass
from architext.core.application.queries.base import Query
from typing import Literal, Optional


@dataclass
class IsNameValidResult:
    is_valid: bool
    error: Optional[Literal['duplicated']]

class IsNameValid(Query[IsNameValidResult]):
    """Check if a name is valid for a new exit or item in the current room."""
    name: str
    in_room_id: Optional[str] = None 
from dataclasses import dataclass
from architext.core.domain.primitives import Visibility

@dataclass(frozen=True)
class Item:
    """Exits are part of the Room aggregate"""
    name: str
    description: str
    visibility: Visibility = "auto"

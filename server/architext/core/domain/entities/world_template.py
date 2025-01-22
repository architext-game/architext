from typing import List, Literal, Optional
from dataclasses import dataclass, field

@dataclass
class WorldTemplate:
    id: str
    name: str
    description: str
    world_encoded_json: str
    author_id: Optional[str]  # null if it is a predefined template
    visibility: Literal["public", "private"] = field(default="private")

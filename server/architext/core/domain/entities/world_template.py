from typing import List, Optional
from dataclasses import dataclass

@dataclass
class WorldTemplate:
    id: str
    name: str
    description: str
    world_encoded_json: str
    author_id: Optional[str]  # null if it is a predefined template

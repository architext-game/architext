from dataclasses import dataclass
from architext.core.application.queries.base import Query
from typing import List, Literal, Dict, Union


@dataclass
class WorldToTextResult:
    world_id: str
    format: Literal['plain', 'encoded']
    text_representation: str

class WorldToText(Query[WorldToTextResult]):
    world_id: str
    format: Literal['plain', 'encoded'] 
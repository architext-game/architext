from dataclasses import dataclass
from typing import Optional, List
from architext.core.application.queries.base import Query


@dataclass
class WorldTemplateListItem:
    id: str
    name: str
    description: str
    author_name: Optional[str]
    author_id: Optional[str]
    you_authorized: bool

@dataclass
class ListWorldTemplatesResult:
    templates: List[WorldTemplateListItem]

class ListWorldTemplates(Query[ListWorldTemplatesResult]):
    pass 
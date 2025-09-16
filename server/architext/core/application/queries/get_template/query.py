from dataclasses import dataclass
from architext.core.application.queries.base import Query
from typing import Optional


@dataclass
class GetWorldTemplateResult:
    id: str
    name: str
    description: str
    owner: Optional[str]

class GetWorldTemplate(Query[GetWorldTemplateResult]):
    template_id: str 
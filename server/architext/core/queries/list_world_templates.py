from dataclasses import dataclass
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
from typing import Optional, List

@dataclass
class TemplateListItem:
    id: str
    name: str
    description: str
    owner: Optional[str]

@dataclass
class ListWorldTemplatesResult:
    templates: List[TemplateListItem]

class ListWorldTemplates(Query[ListWorldTemplatesResult]):
    pass

class ListWorldTemplatesQueryHandler(QueryHandler[ListWorldTemplates, ListWorldTemplatesResult]):
    pass

class UOWListWorldTemplatesQueryHandler(UOWQueryHandler, ListWorldTemplatesQueryHandler):
    def query(self, query: ListWorldTemplates, client_user_id: str) -> ListWorldTemplatesResult:
        return ListWorldTemplatesResult(templates=[TemplateListItem(
            id=template.id,
            description=template.description,
            name=template.name,
            owner=template.author_id
        ) for template in self._uow.world_templates.list_world_templates()])
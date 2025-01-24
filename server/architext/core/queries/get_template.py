from dataclasses import dataclass

from architext.core.authorization import assertUserIsLoggedIn
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
from typing import Optional

@dataclass
class GetWorldTemplateResult:
    id: str
    name: str
    description: str
    owner: Optional[str]

class GetWorldTemplate(Query[GetWorldTemplateResult]):
    template_id: str

class GetWorldTemplateQueryHandler(QueryHandler[GetWorldTemplate, GetWorldTemplateResult]):
    pass

class UOWGetWorldTemplateQueryHandler(UOWQueryHandler, GetWorldTemplateQueryHandler):
    def query(self, query: GetWorldTemplate, client_user_id: str) -> GetWorldTemplateResult:
        assertUserIsLoggedIn(self._uow, client_user_id)
        template = self._uow.world_templates.get_world_template_by_id(query.template_id)
        if template is None:
            raise Exception(f"Template {query.template_id} not found")
        return GetWorldTemplateResult(
            id=template.id,
            description=template.description,
            name=template.name,
            owner=template.author_id
        )
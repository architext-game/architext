from architext.core.application.authorization import assertUserIsLoggedIn
from architext.core.application.queries.base import QueryHandler, UOWQueryHandler
from architext.core.application.queries.get_template.query import GetWorldTemplate, GetWorldTemplateResult


class GetWorldTemplateQueryHandler(QueryHandler[GetWorldTemplate, GetWorldTemplateResult]):
    pass

class UOWGetWorldTemplateQueryHandler(UOWQueryHandler, GetWorldTemplateQueryHandler):
    def query(self, query: GetWorldTemplate, client_user_id: str) -> GetWorldTemplateResult:
        with self._uow as transaction:
            assertUserIsLoggedIn(transaction, client_user_id)
            template = transaction.world_templates.get_world_template_by_id(query.template_id)
            if template is None:
                raise Exception(f"Template {query.template_id} not found")
            return GetWorldTemplateResult(
                id=template.id,
                description=template.description,
                name=template.name,
                owner=template.author_id
            ) 
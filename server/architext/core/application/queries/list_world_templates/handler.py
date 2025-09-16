from architext.core.application.queries.base import QueryHandler, UOWQueryHandler
from architext.core.application.queries.list_world_templates.query import (
    ListWorldTemplates,
    ListWorldTemplatesResult,
    WorldTemplateListItem,
)
from typing import List


class ListWorldTemplatesQueryHandler(QueryHandler[ListWorldTemplates, ListWorldTemplatesResult]):
    pass

class UOWListWorldTemplatesQueryHandler(UOWQueryHandler, ListWorldTemplatesQueryHandler):
    def query(self, query: ListWorldTemplates, client_user_id: str) -> ListWorldTemplatesResult:
        with self._uow as transaction:
            world_templates = ([
                template
                for template in transaction.world_templates.list_world_templates()
                if template.visibility == "public" or template.author_id == client_user_id
            ])
            result: List[WorldTemplateListItem] = []
            for template in world_templates:
                author = transaction.users.get_user_by_id(template.author_id) if template.author_id is not None else None
                author_name = author.name if author is not None else "Architext"
                result.append(WorldTemplateListItem(
                    id=template.id,
                    description=template.description,
                    name=template.name,
                    author_name=author_name,
                    author_id=template.author_id,
                    you_authorized=template.author_id == client_user_id,
                ))
            return ListWorldTemplatesResult(templates=result) 
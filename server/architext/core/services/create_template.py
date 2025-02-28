from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.commands import CreateTemplate, CreateTemplateResult
from uuid import uuid4

from architext.core.queries.world_to_text import WorldToText

from ..authorization import isUserAuthorizedInWorld


def create_template(uow: UnitOfWork, command: CreateTemplate, client_user_id: str) -> CreateTemplateResult:
    world_to_text_result = uow.queries.query(WorldToText(
        format='encoded', world_id=command.base_world_id
    ), client_user_id)
    
    with uow as transaction:
        if not isUserAuthorizedInWorld(transaction, client_user_id, command.base_world_id):
            raise PermissionError("User is not authorized to create a template from that world.")
        
        user = transaction.users.get_user_by_id(client_user_id)
        assert user is not None
        
        text_representation = world_to_text_result.text_representation
        
        template = WorldTemplate(
            id=str(uuid4()),
            name=command.name,
            description=command.description,
            author_id=user.id,
            world_encoded_json=text_representation
        )
        transaction.world_templates.save_world_template(template)
        
    return CreateTemplateResult(
        template_id=template.id
    )

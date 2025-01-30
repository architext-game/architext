from architext.core.domain.events import WorldCreationRequested
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.commands import RequestWorldCreationFromTemplate, RequestWorldCreationFromTemplateResult
import uuid

def request_world_creation_from_template(uow: UnitOfWork, command: RequestWorldCreationFromTemplate, client_user_id: str) -> RequestWorldCreationFromTemplateResult:
    with uow:
        user = uow.users.get_user_by_id(client_user_id)
        assert user is not None
        template = uow.world_templates.get_world_template_by_id(command.template_id)
        assert template is not None

        future_world_id = str(uuid.uuid4())

        uow.external_events.publish(WorldCreationRequested(
            future_world_id=future_world_id,
            user_id=user.id,
            world_name=command.name,
            world_description=command.description,
            text_representation=template.world_encoded_json,
            format='encoded',
            base_template_id=command.template_id,
        ))

        uow.commit()

    return RequestWorldCreationFromTemplateResult(
        future_world_id=future_world_id
    )

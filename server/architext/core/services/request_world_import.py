from architext.core.domain.events import WorldCreationRequested
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.commands import RequestWorldImport, RequestWorldImportResult
import uuid

def request_world_import(uow: UnitOfWork, command: RequestWorldImport, client_user_id: str) -> RequestWorldImportResult:
    with uow as transaction:
        user = transaction.users.get_user_by_id(client_user_id)
        assert user is not None

        future_world_id = str(uuid.uuid4())

        transaction.external_events.publish(WorldCreationRequested(
            future_world_id=future_world_id,
            user_id=user.id,
            world_name=command.name,
            world_description=command.description,
            text_representation=command.text_representation,
            format=command.format,
            visibility='private',
        ))

    return RequestWorldImportResult(
        future_world_id=future_world_id
    )

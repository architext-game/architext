from architext.core.application.commands.delete_template.command import DeleteTemplate, DeleteTemplateResult
from architext.core.application.ports.unit_of_work import UnitOfWork


def delete_template(uow: UnitOfWork, command: DeleteTemplate, client_user_id: str) -> DeleteTemplateResult:
    with uow as transaction:
        user = transaction.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        template = transaction.world_templates.get_world_template_by_id(command.template_id)

        if template is None:
            raise ValueError("Template does not exist")

        if template.author_id != client_user_id:
            raise ValueError("User cannot edit this template.")

        transaction.world_templates.delete_world_template(template.id)

    return DeleteTemplateResult() 
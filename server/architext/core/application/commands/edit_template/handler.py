from architext.core.application.commands.edit_template.command import EditTemplate, EditTemplateResult
from architext.core.application.ports.unit_of_work import UnitOfWork


def edit_template(uow: UnitOfWork, command: EditTemplate, client_user_id: str) -> EditTemplateResult:
    with uow as transaction:
        user = transaction.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        template = transaction.world_templates.get_world_template_by_id(command.template_id)
        
        if template is None:
            raise ValueError("Template does not exist.")

        if template.author_id != client_user_id:
            raise ValueError("User cannot edit this template.")

        if command.name is not None:
            template.name = command.name
        if command.description is not None:
            template.description = command.description

        transaction.world_templates.save_world_template(template)

    return EditTemplateResult() 
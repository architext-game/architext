from architext.core.application.commands.edit_world.command import EditWorld, EditWorldResult
from architext.core.application.ports.unit_of_work import UnitOfWork


def edit_world(uow: UnitOfWork, command: EditWorld, client_user_id: str) -> EditWorldResult:
    with uow as transaction:
        user = transaction.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        world = transaction.worlds.get_world_by_id(command.world_id)
        
        if world is None:
            raise ValueError("World does not exist.")

        if world.owner_user_id != client_user_id:
            raise ValueError("User cannot edit this world.")

        if command.name is not None:
            world.name = command.name
        if command.description is not None:
            world.description = command.description

        transaction.worlds.save_world(world)

    return EditWorldResult() 
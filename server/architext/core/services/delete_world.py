from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.commands import DeleteWorld, DeleteWorldResult
from architext.core.ports.unit_of_work import UnitOfWork


def delete_world(uow: UnitOfWork, command: DeleteWorld, client_user_id: str) -> DeleteWorldResult:
    with uow as transaction:
        assertUserIsAuthorizedInCurrentWorld(transaction, client_user_id)
        user = transaction.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        world = transaction.worlds.get_world_by_id(command.world_id)

        if world is None:
            raise ValueError("World does not exist")

        transaction.worlds.delete_world(world.id)

    return DeleteWorldResult()
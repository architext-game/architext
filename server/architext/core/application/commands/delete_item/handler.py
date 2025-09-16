from architext.core.application.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.application.commands.delete_item.command import DeleteItem, DeleteItemResult
from architext.core.application.ports.unit_of_work import UnitOfWork


def delete_item(uow: UnitOfWork, command: DeleteItem, client_user_id: str) -> DeleteItemResult:
    with uow as transaction:
        assertUserIsAuthorizedInCurrentWorld(transaction, client_user_id)
        user = transaction.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        room = transaction.rooms.get_room_by_id(command.room_id)

        if room is None:
            raise ValueError("Room does not exist")

        item = room.items.get(command.item_name, None)

        if item is None:
            raise ValueError("Item does not exist")
        
        room.remove_item(item)
        transaction.rooms.save_room(room)

    return DeleteItemResult() 
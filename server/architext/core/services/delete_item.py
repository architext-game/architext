from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.commands import DeleteItem, DeleteItemResult
from architext.core.ports.unit_of_work import UnitOfWork


def delete_item(uow: UnitOfWork, command: DeleteItem, client_user_id: str) -> DeleteItemResult:
    with uow:
        assertUserIsAuthorizedInCurrentWorld(uow, client_user_id)
        user = uow.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        room = uow.rooms.get_room_by_id(command.room_id)

        if room is None:
            raise ValueError("Room does not exist")

        item = room.items.get(command.item_name, None)

        if item is None:
            raise ValueError("Item does not exist")
        
        room.remove_item(item)
        uow.rooms.save_room(room)

        uow.commit()

    return DeleteItemResult()
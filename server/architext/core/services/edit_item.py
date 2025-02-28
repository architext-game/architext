from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.commands import EditItem, EditItemResult
from architext.core.domain.entities.item import Item
from architext.core.ports.unit_of_work import UnitOfWork


def edit_item(uow: UnitOfWork, command: EditItem, client_user_id: str) -> EditItemResult:
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
        
        new_item = Item(
            name=command.new_name if command.new_name else item.name,
            description=command.new_description if command.new_description else item.description,
            visibility=command.new_visibility if command.new_visibility else item.visibility,
        )

        room.replace_item(item, new_item)
        transaction.rooms.save_room(room)

    return EditItemResult()
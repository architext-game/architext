from architext.core.authorization import getUserAuthorizedInCurrentWorld
from architext.core.domain.entities.item import Item
from architext.core.commands import CreateItem, CreateItemResult
from architext.core.ports.unit_of_work import UnitOfWork


def create_item(uow: UnitOfWork, command: CreateItem, client_user_id: str = "") -> CreateItemResult:
    user = getUserAuthorizedInCurrentWorld(uow, client_user_id)
    if not user:
        raise PermissionError("User is not in a world where she is authorized.")

    if user.room_id is None:
        raise ValueError("User needs to be in a room to create an item.")

    room = uow.rooms.get_room_by_id(user.room_id)
    if not room:
        raise ValueError(f"Room with id {user.room_id} does not exist.")

    item = Item(
        name=command.name,
        description=command.description,
        visibility=command.visibility,
    )

    room.items.append(item)

    with uow:
        uow.rooms.save_room(room)
        uow.commit()

    return CreateItemResult()

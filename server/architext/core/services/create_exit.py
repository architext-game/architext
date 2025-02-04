from architext.core.authorization import getUserAuthorizedInCurrentWorld
from architext.core.domain.entities.exit import Exit
from architext.core.commands import CreateExit, CreateExitResult
from architext.core.ports.unit_of_work import UnitOfWork


def create_exit(uow: UnitOfWork, command: CreateExit, client_user_id: str = "") -> CreateExitResult:
    user = getUserAuthorizedInCurrentWorld(uow, client_user_id)
    if not user:
        raise PermissionError("User is not in a world where she is authorized.")

    if user.room_id is None:
        raise ValueError("User needs to be in a room to create an exit.")

    room = uow.rooms.get_room_by_id(user.room_id)
    if not room:
        raise ValueError(f"Room with id {user.room_id} does not exist.")

    desitination_room = uow.rooms.get_room_by_id(command.destination_room_id)

    if desitination_room is None:
        raise ValueError(f"Room with id {command.destination_room_id} does not exist.")

    if desitination_room.world_id != room.world_id:
        raise ValueError("Cannot create an exit to a room in another world.")

    exit = Exit(
        name=command.name,
        description=command.description,
        visibility=command.visibility,
        destination_room_id=command.destination_room_id,
    )

    room.exits.append(exit)

    with uow:
        uow.rooms.save_room(room)
        uow.commit()

    return CreateExitResult()

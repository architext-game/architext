from architext.core.application.authorization import getUserAuthorizedInCurrentWorld
from architext.core.domain.entities.exit import Exit
from architext.core.application.commands.create_exit.command import CreateExit, CreateExitResult
from architext.core.application.ports.unit_of_work import UnitOfWork


def create_exit(uow: UnitOfWork, command: CreateExit, client_user_id: str = "") -> CreateExitResult:
    with uow as transaction:
        user = getUserAuthorizedInCurrentWorld(transaction, client_user_id)
        if not user:
            raise PermissionError("User is not in a world where she is authorized.")

        room = transaction.rooms.get_room_by_id(command.in_room_id)
        if not room:
            raise ValueError(f"Room with id {command.in_room_id} does not exist.")

        desitination_room = transaction.rooms.get_room_by_id(command.destination_room_id)

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

        room.add_exit(exit)

        transaction.rooms.save_room(room)

        return CreateExitResult() 
from architext.core.domain.entities.exit import Exit
from architext.ports.unit_of_work import UnitOfWork
from architext.core.commands import ExitInRoom, GetCurrentRoom, GetCurrentRoomResult, CurrentRoom, PersonInRoom


def get_current_room(uow: UnitOfWork, command: GetCurrentRoom, client_user_id: str) -> GetCurrentRoomResult:
    with uow:
        user = uow.users.get_user_by_id(client_user_id)
        if user is None:
            raise ValueError("User not found")
        if user.room_id is None:
            output = GetCurrentRoomResult(current_room=None)
        else:
            current_room = uow.rooms.get_room_by_id(user.room_id)
            if current_room is None:
                raise ValueError("User is not in a room")
            users = uow.users.get_users_in_room(user.room_id)
            people_in_room = [PersonInRoom(id=user.id, name=user.name) for user in users]
            exits_in_room = [ExitInRoom(name=exit.name, description=exit.description) for exit in current_room.exits]
            output = GetCurrentRoomResult(
                current_room=CurrentRoom(
                id=current_room.id,
                exits=exits_in_room,
                description=current_room.description,
                name=current_room.name,
                people=people_in_room
                )
            )
        uow.commit()

    return output
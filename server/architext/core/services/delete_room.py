from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.commands import DeleteRoom, DeleteRoomResult
from architext.core.ports.unit_of_work import UnitOfWork


def delete_room(uow: UnitOfWork, command: DeleteRoom, client_user_id: str) -> DeleteRoomResult:
    with uow:
        assertUserIsAuthorizedInCurrentWorld(uow, client_user_id)
        user = uow.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        if user.room_id is None:
            raise ValueError("User is not in a room.")

        room = uow.rooms.get_room_by_id(user.room_id)

        if room is None:
            raise ValueError("Room does not exist")

        world = uow.worlds.get_world_by_id(room.world_id)
        assert world is not None

        if world.initial_room_id == room.id:
            raise ValueError("The initial room of a world can't be deleted.")
        
        room_id = room.id

        displaced_users = uow.users.get_users_in_room(room_id)

        for user in displaced_users:
            user.room_id = world.initial_room_id
            uow.users.save_user(user)

        uow.rooms.delete_room(room_id)
        uow.rooms.delete_all_exits_leading_to_room(room_id)

        uow.commit()

    return DeleteRoomResult()
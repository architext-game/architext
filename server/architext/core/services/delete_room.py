from architext.core.authorization import assertUserIsAuthorizedInCurrentWorld
from architext.core.commands import DeleteRoom, DeleteRoomResult
from architext.core.ports.unit_of_work import UnitOfWork


def delete_room(uow: UnitOfWork, command: DeleteRoom, client_user_id: str) -> DeleteRoomResult:
    with uow as transaction:
        assertUserIsAuthorizedInCurrentWorld(transaction, client_user_id)
        user = transaction.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        if user.room_id is None:
            raise ValueError("User is not in a room.")

        room = transaction.rooms.get_room_by_id(user.room_id)

        if room is None:
            raise ValueError("Room does not exist")

        world = transaction.worlds.get_world_by_id(room.world_id)
        assert world is not None

        if world.initial_room_id == room.id:
            raise ValueError("The initial room of a world can't be deleted.")
        
        room_id = room.id

        displaced_users = transaction.users.get_users_in_room(room_id)

        for user in displaced_users:
            user.set_room(room_id=world.initial_room_id, world_id=world.id)
            transaction.users.save_user(user)

        transaction.rooms.delete_room(room_id)
        transaction.rooms.delete_all_exits_leading_to_room(room_id)

    return DeleteRoomResult()
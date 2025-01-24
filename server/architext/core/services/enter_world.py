from architext.core.commands import EnterWorld, EnterWorldResult
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import UserChangedRoom


def enter_world(uow: UnitOfWork, command: EnterWorld, client_user_id: str) -> EnterWorldResult:
    with uow:
        user = uow.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")
    
        world = uow.worlds.get_world_by_id(command.world_id)
        
        if world is None:
            raise ValueError("World does not exist.")

        initial_room = uow.rooms.get_room_by_id(world.initial_room_id)
        assert initial_room is not None

        previous_room_id = user.room_id
        user.room_id = initial_room.id
        user.visited_world_ids.add(world.id)
        uow.users.save_user(user)

        uow.publish_events([UserChangedRoom(user_id=user.id, room_entered=initial_room.id, room_left=previous_room_id)])
        uow.commit()

    return EnterWorldResult()
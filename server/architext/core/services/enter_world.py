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

        world_visit_record = user.world_visit_record.get(command.world_id, None)
        if world_visit_record is not None:
            room_to_enter_id = world_visit_record.last_room_id
        else:
            room_to_enter_id = world.initial_room_id

        initial_room = uow.rooms.get_room_by_id(room_to_enter_id)
        assert initial_room is not None

        previous_room_id = user.room_id
        user.set_room(room_id=initial_room.id, world_id=initial_room.world_id)
        uow.users.save_user(user)

        uow.publish_events([UserChangedRoom(
            user_id=user.id,
            method="changed_world",
            room_entered_id=initial_room.id,
            room_left_id=previous_room_id
        )])
        uow.commit()

    return EnterWorldResult()
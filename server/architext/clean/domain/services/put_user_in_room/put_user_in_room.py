from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork
from architext.clean.domain.events.events import UserChangedRoom

def put_user_in_room(uow: UnitOfWork, user_id: str, room_id: str) -> None:
    with uow:
        user = uow.users.get_user_by_id(user_id)
        room = uow.rooms.get_room_by_id(room_id)

        if room is None:
            raise ValueError("The room does not exist")
        
        if user is None:
            raise ValueError("The user does not exist")
        
        user.room_id = room_id
        uow.users.save_user(user)
        uow.publish_events([UserChangedRoom(user_id=user.name, room_entered=room_id, room_left=user.room_id)])
        uow.commit()

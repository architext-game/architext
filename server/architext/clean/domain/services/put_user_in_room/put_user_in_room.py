from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork

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
        uow.commit()

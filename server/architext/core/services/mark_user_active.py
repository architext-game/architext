from architext.core.commands import MarkUserActive, MarkUserActiveResult
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import UserBecameActive, UserBecameInactive


def mark_user_active(uow: UnitOfWork, command: MarkUserActive, client_user_id: str) -> MarkUserActiveResult:
    with uow:
        user = uow.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")

        if user.room_id is None:
            raise ValueError("User is not in a room.")
        
        if user.active == False and command.active == True:
            uow.publish_events([UserBecameActive(
                user_id=user.id,
                room_id=user.room_id,
                user_name=user.name,
            )])
            updated_user = user.with_changes(active=command.active)
            uow.users.save_user(updated_user)
        elif user.active == True and command.active == False:
            uow.publish_events([UserBecameInactive(
                user_id=user.id,
                room_id=user.room_id,
                user_name=user.name,
            )])
            updated_user = user.with_changes(active=command.active)
            uow.users.save_user(updated_user)

        updated_user = user.with_changes(active=command.active)
        uow.users.save_user(updated_user)
        uow.commit()

    return MarkUserActiveResult()
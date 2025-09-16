from architext.core.application.ports.notifier import UserEnteredRoomNotification, UserLeftRoomNotification
from architext.core.application.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import UserBecameInactive


def notify_other_became_inactive(uow: UnitOfWork, event: UserBecameInactive):
    with uow as transaction:
        users = transaction.users.get_users_in_room(event.room_id)
        
        for user in users:
            if user.id == event.user_id:
                continue
            transaction.notifier.notify(user.id, UserLeftRoomNotification(
                user_name=event.user_name,
                movement="disconnected",
                through_exit_name=None,
            ))
        

from architext.core.ports.notifier import UserEnteredRoomNotification
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import UserBecameActive


def notify_other_became_active(uow: UnitOfWork, event: UserBecameActive):
    with uow as transaction:
        users = transaction.users.get_users_in_room(event.room_id)
        
        for user in users:
            if user.id == event.user_id:
                continue
            transaction.notifier.notify(user.id, UserEnteredRoomNotification(
                user_name=event.user_name,
                movement="reconnected",
                through_exit_name=None
            ))
        

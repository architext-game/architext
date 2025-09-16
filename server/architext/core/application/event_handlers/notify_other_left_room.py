from ast import List
from dataclasses import dataclass, asdict
from architext.core.domain.events import ShouldNotifyUserLeftRoom, UserChangedRoom
from architext.core.application.ports.notifier import UserLeftRoomNotification
from architext.core.application.ports.unit_of_work import UnitOfWork


def notify_other_left_room(uow: UnitOfWork, event: UserChangedRoom):
    with uow as transaction:
        if event.room_left_id is None:
            return
        user_who_moved = transaction.users.get_user_by_id(event.user_id)
        assert user_who_moved is not None
        users = transaction.users.get_users_in_room(event.room_left_id)

        for user in users:
            if user.id == event.user_id:
                continue
            transaction.notifier.notify(user.id, UserLeftRoomNotification(
                user_name=user_who_moved.name,
                through_exit_name=event.exit_used_name,
                movement=(
                    'used_exit' if event.exit_used_name is not None else
                    'left_world'
                )
            ))
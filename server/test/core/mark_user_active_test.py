from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake.notifier import FakeNotifier
from architext.core.adapters.fake.uow import FakeUnitOfWork
from architext.core.application.commands import MarkUserActive
from architext.core import Architext
from architext.core.application.ports.notifier import UserEnteredRoomNotification


def test_mark_user_active_success(architext: Architext) -> None:
    command = MarkUserActive(
        active=True
    )
    architext.handle(command, "oliver")

    uow = cast(FakeUnitOfWork, architext._uow)
    with uow as transaction:
        oliver = transaction.users.get_user_by_id("oliver")
        assert oliver is not None
        assert oliver.active is True


def test_mark_user_active_notifies_others_in_room(fake_notifier_architext: Architext, fake_notifier: FakeNotifier) -> None:
    architext = fake_notifier_architext
    with architext._uow as transaction:

        command = MarkUserActive(
            active=True
        )
        architext.handle(command, "evan")

        notifications = fake_notifier.get(notification_type=UserEnteredRoomNotification, user_id="bob")
        print(fake_notifier.sent)
        assert len(notifications) == 1
        notification = notifications[0]
        assert notification.movement == "reconnected"
        assert notification.user_name == "Evan"
        assert notification.through_exit_name is None

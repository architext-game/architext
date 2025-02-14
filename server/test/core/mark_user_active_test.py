from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import MarkUserActive
from architext.core import Architext
from architext.core.ports.notifier import UserEnteredRoomNotification
from test.fixtures import createTestArchitext


@pytest.fixture
def architext() -> Architext:
    return createTestArchitext()


def test_mark_user_active_success(architext: Architext) -> None:
    command = MarkUserActive(
        active=True
    )
    architext.handle(command, "oliver")

    uow = cast(FakeUnitOfWork, architext._uow)
    oliver = uow.users.get_user_by_id("oliver")
    assert oliver is not None
    assert oliver.active is True


def test_mark_user_active_notifies_others_in_room(architext: Architext) -> None:
    notifier = FakeNotifier()
    architext._uow.notifier = notifier

    command = MarkUserActive(
        active=True
    )
    architext.handle(command, "evan")

    notifications = notifier.get(notification_type=UserEnteredRoomNotification, user_id="bob")
    print(notifier.sent)
    assert len(notifications) == 1
    notification = notifications[0]
    assert notification.movement == "reconnected"
    assert notification.user_name == "Evan"
    assert notification.through_exit_name is None

from typing import List, cast
from unittest.mock import Mock
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import TraverseExit, TraverseExitResult
from architext.core.ports.notifier import UserEnteredRoomNotification, UserLeftRoomNotification
from architext.core.ports.unit_of_work import UnitOfWork
import pytest # type: ignore
from architext.core.domain.events import ShouldNotifyUserEnteredRoom, ShouldNotifyUserLeftRoom, UserChangedRoom
from architext.core.messagebus import MessageBus
from architext.core import Architext
from test.fixtures import createTestArchitext, createTestUow


def test_traverse_exit_success(architext: Architext):
    out: TraverseExitResult = architext.handle(TraverseExit(exit_name="To Alice's Room"), client_user_id="oliver")

    assert out.new_room_id == "alices"
    user = architext._uow.users.get_user_by_id("oliver")
    assert user is not None
    assert user.room_id == "alices" 


def test_traverse_exit_user_not_in_room(architext: Architext):
    with pytest.raises(ValueError, match="User is not in a room."):
        architext.handle(TraverseExit(exit_name="To Kitchen"), client_user_id="charlie")


def test_traverse_exit_invalid_exit_name(architext: Architext):
    with pytest.raises(ValueError, match="An exit with that name was not found in the room."):
        architext.handle(TraverseExit(exit_name="Invalid Exit"), client_user_id="alice")


def test_user_changed_room_event_gets_invoked(architext: Architext):
    spy = Mock()
    def handler(uow: FakeUnitOfWork, event: UserChangedRoom):
        assert event.user_id == "alice"
        assert event.room_entered_id == "olivers"
        assert event.room_left_id == "alices"
        assert event.exit_used_name == "To Oliver's Room"
        spy()
    handlers = {UserChangedRoom: [handler]}
    architext._messagebus = MessageBus(event_handlers=handlers)
    architext.handle(TraverseExit(exit_name="To Oliver's Room"), client_user_id="alice")
    assert spy.called


def test_should_notify_user_entered_room(architext: Architext) -> None:
    notifier = FakeNotifier()
    architext._uow.notifier = notifier

    architext.handle(
        command=TraverseExit(
            exit_name="To Oliver's Room"
        ),
        client_user_id="alice"
    )

    notifications = notifier.get(notification_type=UserEnteredRoomNotification, user_id="oliver")
    assert len(notifications) == 1
    notification = notifications[0]
    assert notification.movement == "used_exit"
    assert notification.user_name == "Alice"
    assert notification.through_exit_name == "To Alice's Room"


def test_should_notify_user_left_room(architext: Architext) -> None:
    notifier = FakeNotifier()
    architext._uow.notifier = notifier
    
    architext.handle(
        command=TraverseExit(
            exit_name="To Oliver's Room"
        ),
        client_user_id="dave"
    )

    notifications = notifier.get(notification_type=UserLeftRoomNotification, user_id="bob")

    assert len(notifications) == 1
    notification = notifications[0]
    assert notification.movement == 'used_exit'
    assert notification.user_name == "Dave"
    assert notification.through_exit_name == "To Oliver's Room"


from typing import cast
from unittest.mock import Mock
from architext.core.adapters.fake_notificator import FakeNotificator
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import TraverseExit, TraverseExitResult, CreateInitialData, CreateConnectedRoom, CreateUser
from architext.core.domain.entities.world import DEFAULT_WORLD
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core.domain.entities.exit import Exit
from architext.core.domain.events import UserChangedRoom
from architext.core.messagebus import MessageBus
from architext.core import Architext
from test.fixtures import createTestData


@pytest.fixture
def architext() -> Architext:
    return createTestData()


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
        assert event.user_id is "alice"
        assert event.room_entered is "olivers"
        assert event.room_left is "alices"
        assert event.exit_used is "To Oliver's Room"
        spy()
    handlers = {UserChangedRoom: [handler]}
    architext._messagebus = MessageBus(event_handlers=handlers)
    architext.handle(TraverseExit(exit_name="To Oliver's Room"), client_user_id="alice")
    assert spy.called


def test_users_get_notified_if_other_enters_or_leaves_room(architext: Architext) -> None:
    architext.handle(
        command=TraverseExit(
            exit_name='To Oliver\'s Room'
        ),
        client_user_id="alice"
    )
    notificator = cast(FakeNotificator, architext._uow.notifications)
    assert "oliver" in notificator.notifications
    oliver_notifications = notificator.notifications.get("oliver", None)
    assert oliver_notifications is not None
    assert len(oliver_notifications) == 1
    userb_noti = oliver_notifications[0]
    assert userb_noti.event == 'other_entered_room'
    assert userb_noti.data["user_name"] == 'Alice'

    architext.handle(
        command=TraverseExit(
            exit_name='To Alice\'s Room'
        ),
        client_user_id="oliver"
    )
    assert "alice" in notificator.notifications
    alice_notifications = notificator.notifications.get("alice", None)
    assert alice_notifications is not None
    assert len(alice_notifications) == 1
    userb_noti = alice_notifications[0]
    assert userb_noti.event == 'other_left_room'
    assert userb_noti.data["user_name"] == 'Oliver'

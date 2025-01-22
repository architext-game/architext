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


@pytest.fixture
def architext() -> Architext:
    uow = FakeUnitOfWork()
    room1 = Room(
        id="room1",
        name="Living Room",
        description="A cozy living room",
        exits=[
            Exit(name="To Kitchen", destination_room_id="room2", description="")
        ],
        world_id=DEFAULT_WORLD.id
    )
    room2 = Room(
        id="room2",
        name="Kitchen",
        description="A modern kitchen",
        exits=[],
        world_id=DEFAULT_WORLD.id
    )
    alice = User(
        id="alice",
        name="Alice",
        email="alice@example.com",
        room_id="room1",
        password_hash=b"asdasd"
    )
    bob = User(
        id="bob",
        name="Bob",
        email="bob@example.com",
        room_id=None,
        password_hash=b"asdasd"
    )
    charlie = User(
        id="charlie",
        name="Charle",
        email="charlie@example.com",
        room_id="room1",
        password_hash=b"asdasd"
    )
    dave = User(
        id="dave",
        name="Dave",
        email="dave@example.com",
        room_id="room2",
        password_hash=b"asdasd"
    )
    uow.rooms.save_room(room1)
    uow.rooms.save_room(room2)
    uow.users.save_user(alice)
    uow.users.save_user(bob)
    uow.users.save_user(charlie)
    uow.users.save_user(dave)
    return Architext(uow)


def test_traverse_exit_success(architext: Architext):
    out: TraverseExitResult = architext.handle(TraverseExit(exit_name="To Kitchen"), client_user_id="alice")

    assert out.new_room_id == "room2"
    user = architext._uow.users.get_user_by_id("alice")
    assert user is not None
    assert user.room_id == "room2" 


def test_traverse_exit_user_not_in_room(architext: Architext):
    with pytest.raises(ValueError, match="User is not in a room."):
        architext.handle(TraverseExit(exit_name="To Kitchen"), client_user_id="bob")


def test_traverse_exit_invalid_exit_name(architext: Architext):
    with pytest.raises(ValueError, match="An exit with that name was not found in the room."):
        architext.handle(TraverseExit(exit_name="Invalid Exit"), client_user_id="alice")


def test_user_changed_room_event_gets_invoked(architext: Architext):
    spy = Mock()
    def handler(uow: FakeUnitOfWork, event: UserChangedRoom):
        assert event.user_id is "alice"
        assert event.room_entered is "room2"
        assert event.room_left is "room1"
        assert event.exit_used is "To Kitchen"
        spy()
    handlers = {UserChangedRoom: [handler]}
    architext._messagebus = MessageBus(event_handlers=handlers)
    architext.handle(TraverseExit(exit_name="To Kitchen"), client_user_id="alice")
    assert spy.called


def test_users_get_notified_if_other_enters_or_leaves_room(architext: Architext) -> None:
    architext.handle(
        command=TraverseExit(
            exit_name='To Kitchen'
        ),
        client_user_id="alice"
    )
    notificator = cast(FakeNotificator, architext._uow.notifications)
    assert "charlie" in notificator.notifications
    charlie_notifications = notificator.notifications.get("charlie", None)
    assert charlie_notifications is not None
    assert len(charlie_notifications) == 1
    userb_noti = charlie_notifications[0]
    assert userb_noti.event == 'other_left_room'
    assert userb_noti.data["user_name"] == 'Alice'


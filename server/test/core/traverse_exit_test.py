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
    user1 = User(
        id="in_room",
        name="UserInRoom",
        email="john@example.com",
        room_id="room1",
        password_hash=b"asdasd"
    )
    user2 = User(
        id="not_in_room",
        name="UserNotInRoom",
        email="alice@example.com",
        room_id=None,
        password_hash=b"asdasd"
    )
    uow.rooms.save_room(room1)
    uow.rooms.save_room(room2)
    uow.users.save_user(user1)
    uow.users.save_user(user2)
    return Architext(uow)


def test_traverse_exit_success(architext: Architext):
    out: TraverseExitResult = architext.handle(TraverseExit(exit_name="To Kitchen"), client_user_id="in_room")

    assert out.new_room_id == "room2"
    user = architext._uow.users.get_user_by_id("in_room")
    assert user is not None
    assert user.room_id == "room2" 


def test_traverse_exit_user_not_in_room(architext: Architext):
    with pytest.raises(ValueError, match="User is not in a room."):
        architext.handle(TraverseExit(exit_name="To Kitchen"), client_user_id="not_in_room")


def test_traverse_exit_invalid_exit_name(architext: Architext):
    with pytest.raises(ValueError, match="An exit with that name was not found in the room."):
        architext.handle(TraverseExit(exit_name="Invalid Exit"), client_user_id="in_room")


def test_user_changed_room_event_gets_invoked(architext: Architext):
    spy = Mock()
    def handler(uow: FakeUnitOfWork, event: UserChangedRoom):
        assert event.user_id is "in_room"
        assert event.room_entered is "room2"
        assert event.room_left is "room1"
        assert event.exit_used is "To Kitchen"
        spy()
    handlers = {UserChangedRoom: [handler]}
    architext._messagebus = MessageBus(event_handlers=handlers)
    architext.handle(TraverseExit(exit_name="To Kitchen"), client_user_id="in_room")
    assert spy.called


def test_users_get_notified_if_other_enters_or_leaves_room(architext: Architext) -> None:
    architext.handle(CreateInitialData())
    user_a = architext.handle(CreateUser(
        email='test@test.com',
        name='testerA',
        password='asdasd'
    ))
    user_b = architext.handle(CreateUser(
        email='test@test.com',
        name='testerB',
        password='asdasd'
    ))
    room = architext.handle(
        command=CreateConnectedRoom(
            name='rrom',
            description='descripdsdas',
            exit_to_new_room_name='go',
            exit_to_new_room_description='hehe',
            exit_to_old_room_name='return',
            exit_to_old_room_description='hoho'
        ),
        client_user_id=user_a.user_id
    )
    architext.handle(
        command=TraverseExit(
            exit_name='go'
        ),
        client_user_id=user_a.user_id
    )
    notificator = cast(FakeNotificator, architext._uow.notifications)
    assert user_b.user_id in notificator.notifications
    userb_notifications = notificator.notifications.get(user_b.user_id, None)
    assert userb_notifications is not None
    assert len(userb_notifications) == 1
    userb_noti = userb_notifications[0]
    assert userb_noti.event == 'other_left_room'
    assert userb_noti.data["user_name"] == 'testerA'


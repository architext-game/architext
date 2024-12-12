from unittest.mock import Mock
import pytest
from architext.domain.entities.user import User
from architext.domain.entities.room import Room
from architext.domain.entities.exit import Exit
from architext.domain.unit_of_work.fake.fake_uow import FakeUnitOfWork
from architext.domain.services.traverse_exit.traverse_exit import traverse_exit, TraverseExitInput
from architext.domain.events.events import UserChangedRoom
from architext.domain.events.messagebus import MessageBus


@pytest.fixture
def uow() -> FakeUnitOfWork:
    uow = FakeUnitOfWork()
    room1 = Room(
        id="room1",
        name="Living Room",
        description="A cozy living room",
        exits=[
            Exit(name="To Kitchen", destination_room_id="room2", description="")
        ]
    )
    room2 = Room(
        id="room2",
        name="Kitchen",
        description="A modern kitchen",
        exits=[]
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
        email="Alice@example.com",
        room_id=None,
        password_hash=b"asdasd"
    )
    uow.rooms.save_room(room1)
    uow.rooms.save_room(room2)
    uow.users.save_user(user1)
    uow.users.save_user(user2)
    return uow


def test_traverse_exit_success(uow: FakeUnitOfWork):
    out = traverse_exit(uow, TraverseExitInput(exit_name="To Kitchen"), client_user_id="in_room")

    assert out.new_room_id == "room2"
    user = uow.users.get_user_by_id("in_room")
    assert user is not None
    assert user.room_id == "room2" 


def test_traverse_exit_user_not_in_room(uow: FakeUnitOfWork):
    with pytest.raises(ValueError, match="User is not in a room."):
        traverse_exit(uow, TraverseExitInput(exit_name="To Kitchen"), client_user_id="not_in_room")


def test_traverse_exit_invalid_exit_name(uow: FakeUnitOfWork):
    with pytest.raises(ValueError, match="An exit with that name was not found in the room."):
        traverse_exit(uow, TraverseExitInput(exit_name="Invalid Exit"), client_user_id="in_room")


def test_user_changed_room_event_gets_invoked(uow: FakeUnitOfWork):
    spy = Mock()
    def handler(uow: FakeUnitOfWork, event: UserChangedRoom):
        assert event.user_id is "in_room"
        assert event.room_entered is "room2"
        assert event.room_left is "room1"
        assert event.exit_used is "To Kitchen"
        spy()
    handlers = {UserChangedRoom: [handler]}
    uow.messagebus = MessageBus(handlers=handlers)
    traverse_exit(uow, TraverseExitInput(exit_name="To Kitchen"), client_user_id="in_room")
    assert spy.called


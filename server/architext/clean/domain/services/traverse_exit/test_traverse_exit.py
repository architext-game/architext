from unittest.mock import Mock
import pytest
from architext.clean.domain.entities.user import User
from architext.clean.domain.entities.room import Room
from architext.clean.domain.entities.exit import Exit
from architext.clean.domain.unit_of_work.fake_unit_of_work import FakeUnitOfWork
from architext.clean.domain.services.traverse_exit.traverse_exit import traverse_exit
from architext.clean.domain.events.events import UserChangedRoom
from architext.clean.domain.events.messagebus import MessageBus


@pytest.fixture
def uow() -> FakeUnitOfWork:
    uow = FakeUnitOfWork()
    room1 = Room(
        id="room1",
        name="Living Room",
        description="A cozy living room",
        exits=[
            Exit(name="To Kitchen", destination_room_id="room2", description="", is_open=True, key_names=[], visibility="listed")
        ]
    )
    room2 = Room(
        id="room2",
        name="Kitchen",
        description="A modern kitchen",
        exits=[]
    )
    user1 = User(
        name="UserInRoom",
        email="john@example.com",
        room_id="room1",
        password_hash=b"asdasd"
    )
    user2 = User(
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
    new_room_id = traverse_exit(uow, "UserInRoom", exit_name="To Kitchen")

    assert new_room_id == "room2"
    assert uow.users.get_user_by_id("UserInRoom").room_id == "room2"


def test_traverse_exit_user_not_in_room(uow: FakeUnitOfWork):
    with pytest.raises(ValueError, match="User is not in a room."):
        traverse_exit(uow, "UserNotInRoom", exit_name="To Kitchen")


def test_traverse_exit_invalid_exit_name(uow: FakeUnitOfWork):
    with pytest.raises(ValueError, match="An exit with that name was not found in the room."):
        traverse_exit(uow, "UserInRoom", exit_name="Invalid Exit")


def test_user_changed_room_event_gets_invoked_with_exit_used_null(uow: FakeUnitOfWork):
    spy = Mock()
    def handler(event: UserChangedRoom):
        assert event.user_id is "UserInRoom"
        assert event.room_entered is "room2"
        assert event.room_left is "room1"
        assert event.exit_used is "To Kitchen"
        spy()
    handlers = {UserChangedRoom: [handler]}
    uow.messagebus = MessageBus(handlers=handlers)
    traverse_exit(uow, "UserInRoom", exit_name="To Kitchen")
    assert spy.called


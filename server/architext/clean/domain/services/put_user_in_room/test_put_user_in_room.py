import pytest
from unittest.mock import Mock
from architext.clean.domain.entities.user import User
from architext.clean.domain.entities.room import Room
from architext.clean.domain.unit_of_work.fake_unit_of_work import FakeUnitOfWork
from architext.clean.domain.services.put_user_in_room.put_user_in_room import put_user_in_room
from architext.clean.domain.events.events import UserChangedRoom
from architext.clean.domain.events.messagebus import MessageBus


@pytest.fixture
def uow() -> FakeUnitOfWork:
    uow = FakeUnitOfWork()
    uow.users.save_user(User(id="0", name="John", email="john@example.com", room_id=None, password_hash=b"asd"))
    uow.users.save_user(User(id="1", name="Alice", email="alice@example.com", room_id=None, password_hash=b"asd"))
    uow.rooms.save_room(Room(id="room1", name="Living Room", description="A cozy living room", exits=[]))
    uow.rooms.save_room(Room(id="room2", name="Kitchen", description="A modern kitchen", exits=[]))
    return uow

def test_put_user_in_room_success(uow: FakeUnitOfWork):
    put_user_in_room(uow, user_id="0", room_id="room1")

    user = uow.users.get_user_by_id("0")
    assert uow.committed
    assert user.room_id == "room1"


def test_put_user_in_room_invalid_room(uow: FakeUnitOfWork):
    with pytest.raises(KeyError):
        put_user_in_room(uow, user_id="0", room_id="invalid_room")
    assert not uow.committed


def test_put_user_in_room_invalid_user(uow: FakeUnitOfWork):
    with pytest.raises(KeyError):
        put_user_in_room(uow, user_id="invalid_user", room_id="room1")
    assert not uow.committed


def test_user_changed_room_event_gets_invoked_with_exit_used_null(uow: FakeUnitOfWork):
    spy = Mock()
    def handler(event: UserChangedRoom):
        assert event.exit_used is None
        spy()
    handlers = {UserChangedRoom: [handler]}
    uow.messagebus = MessageBus(handlers=handlers)
    put_user_in_room(uow, user_id="0", room_id="room1")
    assert spy.called

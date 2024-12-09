import pytest
from architext.clean.domain.entities.user import User
from architext.clean.domain.entities.room import Room
from architext.clean.domain.unit_of_work.fake.fake_uow import FakeUnitOfWork
from architext.clean.domain.services.get_current_room.get_current_room import get_current_room


@pytest.fixture
def uow() -> FakeUnitOfWork:
    uow = FakeUnitOfWork()
    uow.rooms.save_room(Room(id="room1", name="Living Room", description="A cozy living room", exits=[]))
    uow.rooms.save_room(Room(id="room2", name="Kitchen", description="A modern kitchen", exits=[]))
    uow.users.save_user(User(id="0", name="John", email="john@example.com", room_id="room1", password_hash=b"asdasd"))
    uow.users.save_user(User(id="1", name="Alice", email="alice@example.com", room_id=None, password_hash=b"asdasd"))
    uow.users.save_user(User(id="2", name="Paul", email="paul@example.com", room_id="room1", password_hash=b"asdasd"))
    return uow


def test_get_current_room_success(uow: FakeUnitOfWork):
    room = get_current_room(uow=uow, client_user_id="0")

    assert room is not None
    assert room.id == "room1"
    assert room.name == "Living Room"
    assert room.description == "A cozy living room"


def test_get_current_room_user_not_in_room(uow: FakeUnitOfWork):
    room = get_current_room(uow=uow, client_user_id="1")
    assert room is None


def test_get_current_room_invalid_user_id(uow: FakeUnitOfWork):
    with pytest.raises(ValueError):
        room = get_current_room(uow=uow, client_user_id="invalid")


def test_get_current_room_lists_people_in_room(uow: FakeUnitOfWork):
    room = get_current_room(uow=uow, client_user_id="0")
    assert room is not None
    assert len(room.people) == 2
    assert "John" in [person.name for person in room.people]

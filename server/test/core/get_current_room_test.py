from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.messagebus import MessageBus
from architext.core.services.get_current_room import get_current_room
from architext.core.commands import GetCurrentRoom, GetCurrentRoomResult
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room


@pytest.fixture
def uow() -> FakeUnitOfWork:
    uow = FakeUnitOfWork()
    uow.rooms.save_room(Room(id="room1", name="Living Room", description="A cozy living room", exits=[]))
    uow.rooms.save_room(Room(id="room2", name="Kitchen", description="A modern kitchen", exits=[]))
    uow.users.save_user(User(id="0", name="John", email="john@example.com", room_id="room1", password_hash=b"asdasd"))
    uow.users.save_user(User(id="1", name="Alice", email="alice@example.com", room_id=None, password_hash=b"asdasd"))
    uow.users.save_user(User(id="2", name="Paul", email="paul@example.com", room_id="room1", password_hash=b"asdasd"))
    return uow

@pytest.fixture
def message_bus() -> MessageBus:
    return MessageBus() 


def test_get_current_room_success(uow: FakeUnitOfWork, message_bus: MessageBus):
    result: GetCurrentRoomResult = message_bus.handle(uow, GetCurrentRoom(), client_user_id="0")

    assert result.current_room is not None
    assert result.current_room.id == "room1"
    assert result.current_room.name == "Living Room"
    assert result.current_room.description == "A cozy living room"


def test_get_current_room_user_not_in_room(uow: FakeUnitOfWork, message_bus: MessageBus):
    result: GetCurrentRoomResult = message_bus.handle(uow, GetCurrentRoom(), client_user_id="1")
    assert result.current_room is None


def test_get_current_room_invalid_user_id(uow: FakeUnitOfWork, message_bus: MessageBus):
    with pytest.raises(ValueError):
        result: GetCurrentRoomResult = message_bus.handle(uow, GetCurrentRoom(), client_user_id="invalid")


def test_get_current_room_lists_people_in_room(uow: FakeUnitOfWork, message_bus: MessageBus):
    result: GetCurrentRoomResult = message_bus.handle(uow, GetCurrentRoom(), client_user_id="0")
    assert result.current_room is not None
    assert len(result.current_room.people) == 2
    assert "John" in [person.name for person in result.current_room.people]

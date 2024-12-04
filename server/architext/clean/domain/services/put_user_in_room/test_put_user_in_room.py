import pytest
from architext.clean.domain.entities.user import User
from architext.clean.domain.entities.room import Room
from architext.clean.domain.unit_of_work.fake_unit_of_work import FakeUnitOfWork
from architext.clean.domain.services.put_user_in_room.put_user_in_room import put_user_in_room


@pytest.fixture
def uow() -> FakeUnitOfWork:
    uow = FakeUnitOfWork()
    uow.users.save_user(User(name="John", email="john@example.com", room_id=None, password_hash=b"asd"))
    uow.users.save_user(User(name="Alice", email="alice@example.com", room_id=None, password_hash=b"asd"))
    uow.rooms.save_room(Room(id="room1", name="Living Room", description="A cozy living room", exits=[]))
    uow.rooms.save_room(Room(id="room2", name="Kitchen", description="A modern kitchen", exits=[]))
    return uow

def test_put_user_in_room_success(uow: FakeUnitOfWork):
    """Test para verificar que un usuario es asignado exitosamente a una habitación."""
    put_user_in_room(uow, user_id="John", room_id="room1")

    user = uow.users.get_user_by_id("John")
    assert uow.committed
    assert user.room_id == "room1"


def test_put_user_in_room_invalid_room(uow: FakeUnitOfWork):
    """Test para verificar que no se puede asignar un usuario a una habitación inexistente."""
    with pytest.raises(KeyError):
        put_user_in_room(uow, user_id="John", room_id="invalid_room")
    assert not uow.committed


def test_put_user_in_room_invalid_user(uow: FakeUnitOfWork):
    """Test para verificar que no se puede asignar una habitación a un usuario inexistente."""
    with pytest.raises(KeyError):
        put_user_in_room(uow, user_id="invalid_user", room_id="room1")
    assert not uow.committed
